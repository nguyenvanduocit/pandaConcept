---
name: preprocess-room
description: Extract depth maps, edge maps, and segmentation from room photos for layout-preserving design generation. Use when the user provides a room photo and wants to redesign it while keeping the same spatial layout.
---

# Preprocess Room Photo

Extract structural control maps from a reference room photo. These maps are used by `/render` to generate new designs that preserve the original room's geometry, proportions, and spatial layout.

## Input Requirements

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room photo path**: path to the source image (from `projects/<name>/references/` or user-provided)
2. **Output directory**: where to save maps (default: `projects/<name>/references/preprocessed/`)
3. **Maps to generate**: depth, canny, mlsd, segmentation, or "all" (default: all)
4. **Project name**: which project this belongs to (ask if not clear from context)

## Preprocessing Pipeline

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

Save all maps to `projects/<name>/references/preprocessed/`:

```
references/preprocessed/
├── depth_map.png        # Grayscale depth (always generated)
├── canny_edge.png       # Edge detection
├── mlsd_lines.png       # Straight line segments
├── segmentation.png     # Semantic zones (colored)
└── metadata.json        # Source image info and parameters used
```

### metadata.json format

```json
{
  "source_image": "references/room_photo.jpg",
  "source_resolution": [1920, 1080],
  "generated_at": "2026-03-23T14:30:00",
  "maps": {
    "depth": {"model": "depth_anything_v2_vitl", "file": "depth_map.png"},
    "canny": {"low_threshold": 100, "high_threshold": 200, "file": "canny_edge.png"},
    "mlsd": {"thr_v": 0.1, "thr_d": 0.1, "file": "mlsd_lines.png"},
    "segmentation": {"model": "segformer-b5-ade-640", "file": "segmentation.png"}
  }
}
```

Always write `metadata.json` after all maps are generated, even if only a subset of maps was requested.

## Dependencies

```
pip install depth-anything-v2 torch torchvision opencv-python controlnet-aux transformers pillow
```

Depth Anything V2 requires model checkpoints downloaded separately (~400MB for vitl). MiDaS downloads automatically via PyTorch Hub on first use.

## Workflow Integration

This skill is the **first step** when working with a reference room photo before any redesign work.

1. User provides a room photo + redesign request
2. Run `/preprocess-room` to extract control maps
3. Pass maps to `/render` for layout-controlled generation (ControlNet / Stability structure control)
4. Optionally use `/validate-layout` to compare spatial layout before and after

For project work: always save maps inside the project's `references/preprocessed/` folder so they are available to all downstream skills.

## Session Relevant Skills

- `/render` — consumes preprocessed maps for layout-controlled generation via ControlNet. Pass the depth map as the primary control signal; add canny or mlsd for sharper architectural edges.
- `/edit-design` — should call `/preprocess-room` first when the user is editing from a photo reference. The segmentation map enables targeted zone editing.
- `/mask-room` — uses the segmentation map to create masked regions for inpainting specific zones (swap floor, repaint walls, etc.).
- `/validate-layout` — uses the depth map to verify that spatial layout is preserved after rendering. Run after `/render` to confirm geometry fidelity.

## Gotchas

- **Depth Anything V2 checkpoints**: must be downloaded manually before first use. If not present, fall back to MiDaS automatically.
- **MiDaS on Mac**: MiDaS via PyTorch Hub does not support `mps` device — use `cpu` fallback on Apple Silicon if errors occur.
- **MLSD scope**: works best for rooms with clearly visible wall/floor/ceiling boundaries. Heavily furnished or cluttered rooms produce sparse line maps — supplement with canny in those cases.
- **Segmentation quality**: open, uncluttered rooms segment more accurately. Dense furniture arrangements may cause label bleed — review the output visually before using for masking.
- **Resolution matching**: control maps must match the target generation resolution. Resize maps to match the provider's expected input size before passing to `/render`.
- **Mac M1/M2**: use `mps` device for GPU acceleration where supported. Fall back to `cpu` if VRAM pressure causes errors.
- **Always write metadata.json**: downstream skills (`/render`, `/validate-layout`) read this file to determine which maps are available and which models were used.
