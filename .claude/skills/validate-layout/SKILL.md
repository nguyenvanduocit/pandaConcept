---
name: validate-layout
description: Verify that AI-generated interior designs preserve the original room layout by comparing depth maps and structural features. Use after rendering to check layout fidelity.
---

# Validate Layout

After generating a new design from a reference room photo, validate that the generated image preserves the original room's spatial layout — wall positions, furniture depth ordering, ceiling height, window placements. Uses depth map comparison (SSIM) and edge similarity as quantitative metrics.

## Pre-flight Checks (MANDATORY — run before validation)

**Before validating**, check what's available to avoid redundant depth extraction.

```
!ls projects/${PROJECT_NAME}/references/preprocessed/depth_map.png 2>/dev/null && echo "HAS_ORIGINAL_DEPTH=true" || echo "HAS_ORIGINAL_DEPTH=false"
```

```
!ls projects/${PROJECT_NAME}/renders/*.png 2>/dev/null && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/notes.md 2>/dev/null && echo "HAS_NOTES=true" || echo "HAS_NOTES=false"
```

### Decision Logic

```
HAS_RENDERS=false?
└── STOP. No renders to validate. Run /render first.

HAS_ORIGINAL_DEPTH=true?
└── Use existing depth map from /preprocess-room — skip re-extraction for the original image.
    Only extract depth for the generated image(s).

HAS_REFERENCE=true AND HAS_ORIGINAL_DEPTH=false?
└── Run /preprocess-room first (depth only) to get baseline depth map.
    OR extract depth inline using MiDaS (slower, but no dependency on /preprocess-room).

HAS_NOTES=true?
└── Read notes.md — check for previous SSIM scores. Compare trends across renders.
    Append new validation results to notes.md.
```

**Reuse the original depth map whenever possible** — depth extraction is the most expensive step.

## Input

- Original room photo (or its preprocessed depth map from `/preprocess-room`)
- Generated design image(s) from `/render`
- Threshold for acceptable layout preservation (default: SSIM >= 0.70)

## Validation Pipeline

### Step 1: Extract Depth Maps

If preprocessed maps don't exist, generate them for both images.

```python
import torch, cv2, numpy as np
from PIL import Image

def get_depth_map(image_path: str) -> np.ndarray:
    """Extract depth map using MiDaS."""
    model = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid")
    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_batch = transforms.dpt_transform(img_rgb).to(device)

    with torch.no_grad():
        prediction = model(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1), size=img_rgb.shape[:2],
            mode="bicubic", align_corners=False
        ).squeeze()

    depth = prediction.cpu().numpy()
    return ((depth - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)
```

### Step 2: SSIM Comparison (Primary Metric)

```python
from skimage.metrics import structural_similarity as ssim
import numpy as np

def compare_depth_ssim(original_depth: np.ndarray, generated_depth: np.ndarray) -> dict:
    """Compare two depth maps using SSIM. Higher = better layout preservation."""
    # Ensure same size
    if original_depth.shape != generated_depth.shape:
        from PIL import Image
        generated_depth = np.array(
            Image.fromarray(generated_depth).resize(
                (original_depth.shape[1], original_depth.shape[0]),
                resample=Image.BILINEAR
            )
        )

    score, diff_map = ssim(original_depth, generated_depth, full=True)
    return {
        "ssim_score": round(score, 4),
        "interpretation": interpret_ssim(score),
        "diff_map": ((1 - diff_map) * 255).astype(np.uint8)  # Highlights differences
    }

def interpret_ssim(score: float) -> str:
    if score >= 0.85: return "Excellent — layout nearly identical"
    if score >= 0.70: return "Good — layout preserved with minor variations"
    if score >= 0.55: return "Fair — noticeable layout differences"
    if score >= 0.40: return "Poor — significant layout deviation"
    return "Failed — layout not preserved"
```

### Step 3: Edge Similarity (Secondary Metric)

```python
import cv2, numpy as np

def compare_edges(original_path: str, generated_path: str) -> dict:
    """Compare Canny edges to check architectural feature preservation."""
    def get_edges(path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return cv2.Canny(cv2.GaussianBlur(img, (5,5), 0), 100, 200)

    edges_orig = get_edges(original_path)
    edges_gen = get_edges(generated_path)

    # Resize if needed
    if edges_orig.shape != edges_gen.shape:
        edges_gen = cv2.resize(edges_gen, (edges_orig.shape[1], edges_orig.shape[0]))

    # IoU of edge pixels
    intersection = np.logical_and(edges_orig > 0, edges_gen > 0).sum()
    union = np.logical_or(edges_orig > 0, edges_gen > 0).sum()
    iou = intersection / union if union > 0 else 0

    return {
        "edge_iou": round(iou, 4),
        "interpretation": "Good" if iou >= 0.15 else "Low edge overlap"
    }
```

### Step 4: Full Validation Report

```python
def validate_layout(original_path: str, generated_path: str) -> dict:
    """Run full layout validation pipeline."""
    orig_depth = get_depth_map(original_path)
    gen_depth = get_depth_map(generated_path)

    depth_result = compare_depth_ssim(orig_depth, gen_depth)
    edge_result = compare_edges(original_path, generated_path)

    overall_pass = depth_result["ssim_score"] >= 0.70

    return {
        "overall": "PASS" if overall_pass else "FAIL",
        "depth_ssim": depth_result,
        "edge_similarity": edge_result,
        "recommendation": (
            "Layout preserved — proceed with refinement" if overall_pass
            else "Layout deviation detected — consider re-rendering with higher ControlNet strength"
        )
    }
```

## Output Format

```
## Layout Validation Report

### Original: references/room_photo.jpg
### Generated: renders/scandinavian_stability_20260323.png

| Metric | Score | Rating |
|--------|-------|--------|
| Depth SSIM | 0.82 | Good |
| Edge IoU | 0.23 | Good |
| Overall | PASS | Layout preserved |

### Difference Map
[Saved to: references/preprocessed/layout_diff.png]
Bright areas = layout differences. Dark = preserved.

### Recommendations
- Layout well preserved overall
- Minor deviation in left wall area — furniture placement shifted slightly
- Suggest: increase ControlNet conditioning_scale to 0.90 for tighter layout control
```

## SSIM Thresholds for Interior Design

| Score | Rating | What It Means |
|-------|--------|---------------|
| >= 0.85 | Excellent | Room geometry nearly identical — walls, windows, doors all match |
| 0.70–0.84 | Good | Layout preserved — minor furniture position/size variations acceptable |
| 0.55–0.69 | Fair | Noticeable changes — room shape similar but furniture rearranged |
| 0.40–0.54 | Poor | Significant deviation — room proportions may have changed |
| < 0.40 | Failed | Different room — layout not preserved at all |

## Session Relevant Skills

- `/preprocess-room` — generates the original depth map (skip re-extraction if exists)
- `/render` — re-render with higher ControlNet strength if validation fails
- `/compare-models` — add layout SSIM score to provider comparison
- `/refine` — if layout is good but style needs work, refine the prompt

## Gotchas

- SSIM compares structure, not style — a perfect layout match with different colors will score high (correct behavior)
- Depth maps are relative, not absolute — two photos of the same room from slightly different angles will have lower SSIM even though it's the same room
- Edge IoU is intentionally low threshold (0.15) because style changes legitimately change many edges (different furniture shapes)
- Always compare at the same resolution — resize generated to match original before comparing
- If using img2img (not ControlNet), expect lower SSIM scores (0.55-0.70 is good for img2img)

## Dependencies

```
pip install scikit-image torch torchvision opencv-python pillow
```
