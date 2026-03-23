---
name: mask-room
description: Create precise masks for targeted room editing using SAM2 segmentation. Use when the user wants to change specific elements (furniture, walls, floor) while keeping everything else intact.
---

# Mask Room Elements for Inpainting

Generate precise binary masks that isolate specific room elements for inpainting. Instead of regenerating the entire room, masks allow surgical edits — change only the sofa, repaint only the walls, replace only the flooring — while preserving everything else pixel-perfectly.

## Pre-flight Checks (MANDATORY — run before masking)

**Before masking**, check what resources are available to choose the best method.

```
!ls projects/${PROJECT_NAME}/references/preprocessed/segmentation.png 2>/dev/null && echo "HAS_SEGMENTATION=true" || echo "HAS_SEGMENTATION=false"
```

```
!ls projects/${PROJECT_NAME}/references/masks/*.png 2>/dev/null && echo "HAS_EXISTING_MASKS=true" || echo "HAS_EXISTING_MASKS=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/renders/*.png 2>/dev/null && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"
```

### Decision Logic

```
HAS_REFERENCE=false AND HAS_RENDERS=false?
└── STOP. No source image to mask. Ask user to provide an image.

HAS_EXISTING_MASKS=true?
└── List existing masks. Ask user: reuse existing mask, create new one, or combine?

Target is a zone (wall, floor, ceiling) AND HAS_SEGMENTATION=true?
└── Use Method 3 (Semantic Auto-Mask from segmentation) — fastest, no interaction needed.

Target is a zone BUT HAS_SEGMENTATION=false?
└── Run /preprocess-room first (segmentation only) — then use Method 3.
    OR fall back to Method 1/2 (SAM2 point/box) if user prefers immediate results.

Target is a specific object (sofa, lamp, plant)?
└── Use Method 1 (SAM2 Point) or Method 2 (SAM2 Box) — segmentation too coarse for individual objects.
```

**Choose the lightest method that achieves the goal.** Zone masking from segmentation is instant; SAM2 requires model loading.

## Input

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room photo**: original or rendered image to mask
2. **Target element(s)**: what to isolate — "sofa", "walls", "floor", "ceiling", "windows", or custom description
3. **Mask output path** (default: `references/masks/`)

## Masking Methods

### Method 1: SAM2 Point-Prompted (Interactive)

Best for specific objects. User clicks approximate center of the element.

```python
import numpy as np
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

def mask_by_point(image_path: str, point_xy: tuple, output_path: str):
    """Mask an element by clicking its approximate center."""
    model = build_sam2("sam2_hiera_l.yaml", "checkpoints/sam2_hiera_large.pt")
    predictor = SAM2ImagePredictor(model)

    image = np.array(Image.open(image_path).convert("RGB"))
    predictor.set_image(image)

    point = np.array([[point_xy[0], point_xy[1]]])
    masks, scores, _ = predictor.predict(
        point_coords=point,
        point_labels=np.array([1]),
        multimask_output=True
    )
    best_mask = masks[np.argmax(scores)]

    # Save as binary mask (white = edit zone, black = keep)
    mask_img = Image.fromarray((best_mask * 255).astype(np.uint8))
    mask_img.save(output_path)
    return best_mask
```

### Method 2: SAM2 Box-Prompted

Best for rectangular regions or when point prompting is ambiguous.

```python
def mask_by_box(image_path: str, box_xyxy: tuple, output_path: str):
    """Mask an element by bounding box [x1, y1, x2, y2]."""
    model = build_sam2("sam2_hiera_l.yaml", "checkpoints/sam2_hiera_large.pt")
    predictor = SAM2ImagePredictor(model)

    image = np.array(Image.open(image_path).convert("RGB"))
    predictor.set_image(image)

    box = np.array([list(box_xyxy)])
    masks, scores, _ = predictor.predict(
        box=box,
        multimask_output=True
    )
    best_mask = masks[np.argmax(scores)]
    mask_img = Image.fromarray((best_mask * 255).astype(np.uint8))
    mask_img.save(output_path)
    return best_mask
```

### Method 3: Semantic Auto-Mask (from /preprocess-room segmentation)

Best for masking entire zones (all walls, entire floor, all ceiling).

```python
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
import torch, numpy as np
from PIL import Image

# ADE20K label mapping for common room elements
ROOM_ZONES = {
    "wall": [0], "floor": [3], "ceiling": [5],
    "window": [8], "door": [14], "sofa": [23],
    "table": [33], "chair": [19], "bed": [7],
    "cabinet": [35], "lamp": [36], "curtain": [18],
    "painting": [22], "shelf": [24], "rug": [28]
}

def mask_by_zone(image_path: str, zone: str, output_path: str):
    """Mask an entire semantic zone (e.g., all walls, entire floor)."""
    processor = SegformerImageProcessor.from_pretrained("nvidia/segformer-b5-finetuned-ade-640-640")
    model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b5-finetuned-ade-640-640")

    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    seg_map = outputs.logits.argmax(dim=1).squeeze().numpy()
    seg_resized = np.array(Image.fromarray(seg_map.astype(np.uint8)).resize(image.size, resample=Image.NEAREST))

    labels = ROOM_ZONES.get(zone.lower(), [])
    mask = np.isin(seg_resized, labels).astype(np.uint8) * 255
    Image.fromarray(mask).save(output_path)
```

## Mask Post-Processing

```python
import cv2, numpy as np
from PIL import Image

def refine_mask(mask_path: str, output_path: str, dilate_px: int = 5, feather_px: int = 3):
    """Clean up mask: remove small holes, smooth edges, add feathering."""
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Fill small holes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_px, dilate_px))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Smooth edges
    mask = cv2.GaussianBlur(mask, (feather_px*2+1, feather_px*2+1), 0)

    # Re-threshold
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    cv2.imwrite(output_path, mask)
```

## Using Masks with Providers

### Stability AI Inpainting

```python
import requests

def inpaint_stability(image_path, mask_path, prompt, api_key):
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"image": open(image_path, "rb"), "mask": open(mask_path, "rb")},
        data={"prompt": prompt, "output_format": "png"}
    )
    return response.content
```

### OpenAI DALL-E Edit

```python
from openai import OpenAI

def inpaint_openai(image_path, mask_path, prompt):
    client = OpenAI()
    response = client.images.edit(
        image=open(image_path, "rb"),
        mask=open(mask_path, "rb"),
        prompt=prompt,
        size="1024x1024"
    )
    return response.data[0].url
```

## Output

```
references/masks/
├── wall_mask.png          # Binary mask: white = walls
├── floor_mask.png         # Binary mask: white = floor
├── sofa_mask.png          # Binary mask: white = sofa area
├── custom_mask.png        # User-prompted mask
└── mask_overlay.png       # Visualization: original + mask overlay
```

## Workflow

1. User identifies what to change: "change just the sofa" or "repaint the walls"
2. `/mask-room` generates precise binary mask for that element
3. `/render` uses mask + prompt for inpainting (Stability AI or OpenAI)
4. Only masked area changes — rest of image preserved pixel-perfectly

## Session Relevant Skills

- `/preprocess-room` — generates segmentation map that `/mask-room` can use for zone-based masking
- `/render` — consumes masks for inpainting API calls
- `/edit-design` — generates the edit prompt; `/mask-room` generates the mask; `/render` executes
- `/validate-layout` — verify masked edits preserved layout

## Gotchas

- SAM2 requires ~2GB model checkpoint download
- Point prompts work best when clicking near the CENTER of the object
- For walls: may need multiple points (one per visible wall section) and combine masks
- Mask must be same resolution as source image
- White = area to EDIT, Black = area to KEEP (standard inpainting convention)
- Feathering the mask edges by 3-5px produces smoother inpainting transitions
- Some providers require RGBA PNG with transparency instead of separate mask — check provider docs

## Dependencies

```
pip install sam2 torch torchvision transformers opencv-python pillow
```
