---
name: preprocess-room
description: Full room photo analysis — semantic understanding via Gemini Vision (style, colors, materials, fixtures, prompt) AND structural control maps (depth, canny, segmentation) for layout-preserving design generation. Use when the user provides a room photo for redesign, project init, or any image analysis task.
---

# Preprocess Room Photo

Two-phase analysis of a reference room photo:
1. **Semantic analysis** (Gemini Vision) — understand WHAT is in the room: style, colors, materials, fixtures, lighting → auto-fill project config files
2. **Structural analysis** (depth/edge/segmentation) — understand WHERE things are: geometry, proportions, spatial layout → control maps for layout-preserving rendering

## Pre-flight Checks (MANDATORY — run before any processing)

**Before doing anything**, check what already exists to avoid redundant work.

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/metadata.json 2>/dev/null && echo "HAS_METADATA=true" || echo "HAS_METADATA=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/depth_map.png 2>/dev/null && echo "HAS_DEPTH=true" || echo "HAS_DEPTH=false"
```

### Decision Logic

```
HAS_REFERENCE=false?
└── STOP. No reference image found. Ask user to provide a room photo first.

HAS_METADATA=true AND HAS_SEMANTIC=true AND HAS_DEPTH=true?
└── ALREADY PREPROCESSED. Report what exists and ask:
    - "Preprocessed data đã có từ [date]. Chạy lại (overwrite) hay dùng data hiện tại?"
    - If user says keep → SKIP. Do not re-process.
    - If user says re-run → proceed normally (overwrite).

HAS_SEMANTIC=true BUT HAS_DEPTH=false?
└── Phase 1 done, Phase 2 missing. Run Phase 2 ONLY (structural maps).

HAS_DEPTH=true BUT HAS_SEMANTIC=false?
└── Phase 2 done, Phase 1 missing. Run Phase 1 ONLY (Gemini Vision).

Neither exists?
└── Run both phases.
```

**This prevents wasted API calls and GPU time.** Preprocessing is expensive — never re-run without reason.

## Input Requirements

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room photo path**: path to the source image (from `projects/<name>/references/` or user-provided)
2. **Output directory**: where to save maps (default: `projects/<name>/references/preprocessed/`)
3. **Maps to generate**: depth, canny, mlsd, segmentation, or "all" (default: all)
4. **Project name**: which project this belongs to (ask if not clear from context)

## Phase 1: Semantic Analysis (Gemini Vision — always run first)

Use Gemini Vision API to analyze the room photo and extract semantic understanding. This step auto-fills project config files (`brief.md`, `rooms.md`, `style-config.yaml`, `notes.md`).

**API**: Google Gemini 3.1 Flash (multimodal)
**SDK**: `google-genai` (NOT the deprecated `google.generativeai`)
**API Key**: Read from `GEMINI_API_KEY` env var or from `CLAUDE.local.md`

### Gemini Vision Analysis

```python
from google import genai
from google.genai import types
from PIL import Image
import os, json

def analyze_room_semantic(image_path: str, api_key: str) -> dict:
    """Analyze room photo with Gemini Vision, return structured data."""
    client = genai.Client(api_key=api_key)
    image = Image.open(image_path)

    response = client.models.generate_content(
        model='gemini-3.1-flash-image-preview',
        contents=[image,
        """Analyze this interior design image in detail. Return a JSON object:
{
  "room_type": "type of room",
  "style_analysis": {
    "primary_style": "closest interior design style",
    "secondary_style": "secondary influence or null",
    "style_confidence": "high/medium/low",
    "style_keywords": ["keywords"]
  },
  "color_palette": {
    "primary": "#hex - dominant color",
    "secondary": "#hex - second most prominent",
    "accent": "#hex - accent color",
    "neutrals": ["#hex", "#hex", "#hex"]
  },
  "materials": ["every material visible"],
  "furniture_and_fixtures": ["every piece and fixture"],
  "lighting": {
    "type": "natural/artificial/mixed",
    "mood": "warm/cool/neutral",
    "sources": ["light sources"],
    "time_of_day": "estimated time"
  },
  "spatial": {
    "dimensions_estimate": "small/medium/large",
    "ceiling_height": "standard/high/double",
    "layout": "spatial layout description",
    "camera_angle": "eye-level/low/high/bird-eye",
    "camera_position": "description"
  },
  "surfaces": {
    "walls": "material and finish",
    "floor": "material and finish",
    "ceiling": "material and finish"
  },
  "detailed_description": "3-4 sentence description",
  "image_generation_prompt": "150-200 word optimized prompt for AI image generation. Include all visual details, materials, lighting, camera angle, style keywords. Photorealistic.",
  "negative_prompt": "things to exclude"
}
Return ONLY valid JSON, no markdown."""
    ])

    result = response.text.strip()
    if result.startswith('```'):
        lines = result.split('\n')
        result = '\n'.join(lines[1:])
        if result.endswith('```'):
            result = result[:-3].strip()
    return json.loads(result)
```

### Auto-fill Project Config

After Gemini analysis, update project files with the extracted data:

1. **`style-config.yaml`** — Fill `primary_style`, `secondary_style`, `color_palette`, `materials`, `lighting`, `photography` (camera angle, lens), `negative_prompts`
2. **`rooms.md`** — Fill room type, layout, surfaces (walls/floor/ceiling), furniture & fixtures list, lighting details, render status table
3. **`brief.md`** — Fill style direction, mood/atmosphere, color/material preferences, reference image table, style keywords
4. **`notes.md`** — Save full Gemini analysis: detailed description, image generation prompt (ready to use), negative prompt, analysis metadata (model, date, confidence)

### Semantic Output

Save raw analysis to `projects/<name>/references/preprocessed/`:

```
references/preprocessed/
├── semantic_analysis.json   # Full Gemini Vision output (NEW)
├── depth_map.png            # (Phase 2)
├── ...
```

The `semantic_analysis.json` is consumed by `/generate-prompt`, `/design-consult`, `/edit-design`, and `/refine` to avoid re-analyzing the same image.

---

## Phase 2: Structural Analysis (Control Maps)

Run each requested map in sequence. Always generate depth first — it is the most universally useful for ControlNet-based generation.

### 1. Depth Map (Primary — always generate)

Use Depth Anything V2 (preferred) for highest quality. Fall back to MiDaS if checkpoints are unavailable.

```python
# pip install depth-anything-v2 torch torchvision
import cv2, torch, numpy as np
from PIL import Image
from depth_anything_v2.dpt import DepthAnythingV2

def extract_depth(image_path: str, output_path: str):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    model = DepthAnythingV2(encoder='vitl', features=256, out_channels=[256, 512, 1024, 1024])
    model.load_state_dict(torch.load('checkpoints/depth_anything_v2_vitl.pth', map_location='cpu'))
    model = model.to(DEVICE).eval()

    raw_img = cv2.imread(image_path)
    depth = model.infer_image(raw_img)
    depth_norm = ((depth - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)
    Image.fromarray(depth_norm).convert("RGB").save(output_path)
```

**MiDaS fallback** (downloads automatically via PyTorch Hub — no checkpoint needed):

```python
import torch, cv2, numpy as np
from PIL import Image

def extract_depth_midas(image_path: str, output_path: str):
    model = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = transforms.dpt_transform
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_batch = transform(img_rgb).to(device)

    with torch.no_grad():
        prediction = model(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1), size=img_rgb.shape[:2],
            mode="bicubic", align_corners=False
        ).squeeze()

    depth = prediction.cpu().numpy()
    depth_norm = ((depth - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)
    Image.fromarray(depth_norm).convert("RGB").save(output_path)
```

### 2. Canny Edge Map

Fast OpenCV edge detection. Best for preserving door frames, window outlines, and architectural details.

```python
import cv2, numpy as np
from PIL import Image

def extract_canny(image_path: str, output_path: str, low=100, high=200):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, low, high)
    Image.fromarray(np.stack([edges]*3, axis=2)).save(output_path)
```

### 3. MLSD Line Segment Detection

Best for rectilinear rooms — preserves wall, ceiling, and floor boundary lines.

```python
from controlnet_aux import MLSDdetector
from PIL import Image

def extract_mlsd(image_path: str, output_path: str):
    mlsd = MLSDdetector.from_pretrained("lllyasviel/ControlNet")
    image = Image.open(image_path).convert("RGB")
    mlsd_image = mlsd(image, thr_v=0.1, thr_d=0.1)
    mlsd_image.save(output_path)
```

### 4. Segmentation Map

ADE20K semantic segmentation for full room parsing: wall, floor, ceiling, window, door, and furniture zones.

```python
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
import torch, numpy as np
from PIL import Image

ADE20K_ROOM_LABELS = {
    0: (120, 120, 120),   # wall
    3: (80, 50, 50),      # floor
    5: (6, 230, 230),     # ceiling
    8: (4, 200, 3),       # windowpane
    14: (255, 5, 153),    # door
    15: (204, 5, 255),    # table
    18: (230, 230, 230),  # curtain
    23: (140, 120, 240),  # sofa
    24: (250, 0, 0),      # chair
}

def extract_segmentation(image_path: str, output_path: str):
    processor = SegformerImageProcessor.from_pretrained("nvidia/segformer-b5-finetuned-ade-640-640")
    model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b5-finetuned-ade-640-640")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    seg_map = outputs.logits.argmax(dim=1).squeeze().numpy()
    seg_resized = np.array(Image.fromarray(seg_map.astype(np.uint8)).resize(image.size, resample=Image.NEAREST))
    color_seg = np.zeros((*seg_resized.shape, 3), dtype=np.uint8)
    for label, color in ADE20K_ROOM_LABELS.items():
        color_seg[seg_resized == label] = color
    Image.fromarray(color_seg).save(output_path)
```

## Output

Save all outputs to `projects/<name>/references/preprocessed/`:

```
references/preprocessed/
├── semantic_analysis.json  # Gemini Vision output (Phase 1 — always generated)
├── depth_map.png           # Grayscale depth (Phase 2 — always generated)
├── canny_edge.png          # Edge detection
├── mlsd_lines.png          # Straight line segments
├── segmentation.png        # Semantic zones (colored)
└── metadata.json           # Source image info and parameters used
```

### metadata.json format

```json
{
  "source_image": "references/room_photo.jpg",
  "source_resolution": [1920, 1080],
  "generated_at": "2026-03-23T14:30:00",
  "semantic": {
    "model": "gemini-3.1-flash-image-preview",
    "file": "semantic_analysis.json",
    "style_detected": "contemporary",
    "confidence": "high"
  },
  "maps": {
    "depth": {"model": "depth_anything_v2_vitl", "file": "depth_map.png"},
    "canny": {"low_threshold": 100, "high_threshold": 200, "file": "canny_edge.png"},
    "mlsd": {"thr_v": 0.1, "thr_d": 0.1, "file": "mlsd_lines.png"},
    "segmentation": {"model": "segformer-b5-ade-640", "file": "segmentation.png"}
  }
}
```

Always write `metadata.json` after all phases complete, even if only a subset was requested.

## Dependencies

```
# Phase 1 (Semantic)
pip install google-generativeai

# Phase 2 (Structural)
pip install depth-anything-v2 torch torchvision opencv-python controlnet-aux transformers pillow
```

- Gemini API key required for Phase 1 (from `GEMINI_API_KEY` env var or `CLAUDE.local.md`)
- Depth Anything V2 requires model checkpoints downloaded separately (~400MB for vitl). MiDaS downloads automatically via PyTorch Hub on first use.

## Workflow Integration

This skill is the **first step** when working with a reference room photo — for both project init AND redesign.

### Execution Order

1. **Phase 1 (Semantic)**: Gemini Vision analyzes image → auto-fills project config files + saves `semantic_analysis.json`
2. **Phase 2 (Structural)**: Extract depth/canny/mlsd/segmentation → saves control maps

### When to run which phase

| Scenario | Phase 1 (Semantic) | Phase 2 (Structural) |
|----------|-------------------|---------------------|
| Project init from photo | YES | Optional (run later if redesign needed) |
| Redesign keeping layout | YES (if not done) | YES |
| Quick image understanding | YES | NO |
| Layout validation only | NO | YES (depth only) |

### Downstream flow

```
/preprocess-room (Phase 1 + Phase 2)
    ├── semantic_analysis.json → consumed by /generate-prompt, /design-consult, /edit-design, /refine
    ├── depth_map.png → consumed by /render (structure control), /validate-layout
    ├── canny_edge.png → consumed by /render (edge control)
    └── segmentation.png → consumed by /mask-room, /edit-design
```

For project work: always save outputs inside the project's `references/preprocessed/` folder so they are available to all downstream skills.

## Session Relevant Skills

- `/generate-prompt` — consumes `semantic_analysis.json` to build provider-optimized prompts with accurate style, materials, and lighting from the analysis.
- `/design-consult` — reads semantic analysis to pre-fill style recommendations instead of asking from scratch.
- `/edit-design` — should call `/preprocess-room` first when editing from a photo reference. Uses both semantic (what to change) and structural (where) data.
- `/render` — consumes control maps for layout-controlled generation via ControlNet. Pass depth map as primary control signal; add canny or mlsd for sharper architectural edges.
- `/mask-room` — uses the segmentation map to create masked regions for inpainting specific zones.
- `/validate-layout` — uses the depth map to verify spatial layout is preserved after rendering.
- `/refine` — reads semantic analysis to understand original room context when refining prompts.

## Gotchas

- **Gemini API key**: Phase 1 requires a valid `GEMINI_API_KEY`. If expired or missing, skip Phase 1 and warn user — Phase 2 can still run independently.
- **Gemini rate limits**: Free tier has RPM limits. If rate-limited, retry after delay or ask user to use a paid key.
- **`google.generativeai` is DEPRECATED**: Use `google.genai` (`pip install google-genai`). Import as `from google import genai`. The old `google.generativeai` package no longer receives updates and is missing critical features like `response_modalities`.
- **Depth Anything V2 checkpoints**: must be downloaded manually before first use. If not present, fall back to MiDaS automatically.
- **MiDaS on Mac**: MiDaS via PyTorch Hub does not support `mps` device — use `cpu` fallback on Apple Silicon if errors occur.
- **MLSD scope**: works best for rooms with clearly visible wall/floor/ceiling boundaries. Heavily furnished or cluttered rooms produce sparse line maps — supplement with canny in those cases.
- **Segmentation quality**: open, uncluttered rooms segment more accurately. Dense furniture arrangements may cause label bleed — review the output visually before using for masking.
- **Resolution matching**: control maps must match the target generation resolution. Resize maps to match the provider's expected input size before passing to `/render`.
- **Mac M1/M2**: use `mps` device for GPU acceleration where supported. Fall back to `cpu` if VRAM pressure causes errors.
- **Always write metadata.json**: downstream skills (`/render`, `/validate-layout`, `/generate-prompt`) read this file to determine which outputs are available.
