---
name: render
description: Send image generation prompts to AI providers and collect outputs. Use when the user wants to actually generate interior design images via API calls.
---

# Render Interior Design Images

Execute image generation by sending prompts to AI provider APIs and managing the output.

## Prerequisites

- API keys configured in environment variables (see CLAUDE.md)
- Python environment with provider SDKs installed

## Workflow

### Step 1: Input
Accept via `$ARGUMENTS` or ask:
- **Prompt**: a ready-to-use prompt (or reference a previous `/generate-prompt` output)
- **Provider(s)**: which AI provider(s) to use — or "all" for comparison
- **Parameters**: image size, quality, number of variations

### Step 2: Provider-Specific API Calls

For each provider, construct the appropriate API call:

**OpenAI (DALL-E 3)**:
```python
from openai import OpenAI
client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",  # wide for rooms
    quality="hd",
    n=1
)
```

**Google Gemini (Imagen)**:
```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-exp")  # or imagen model
response = model.generate_content(prompt)
```

**Stability AI**:
```python
import requests
response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"none": ""},
    data={"prompt": prompt, "negative_prompt": negative, "output_format": "png"}
)
```

**Grok (xAI)**:
```python
from openai import OpenAI  # xAI uses OpenAI-compatible API
client = OpenAI(api_key=os.environ["GROK_API_KEY"], base_url="https://api.x.ai/v1")
response = client.images.generate(model="grok-2-image", prompt=prompt)
```

### Step 2B: Layout-Controlled Rendering (when reference photo exists)

When the project has preprocessed control maps (from `/preprocess-room`), use layout-controlled APIs instead of plain text-to-image. These APIs accept a reference image (depth map or edge map) alongside the prompt, allowing the model to preserve the original room's spatial structure while applying the new design style.

**Stability AI Structure Control** (recommended — no GPU needed):
```python
import requests

def render_with_structure(prompt, reference_image_path, api_key, control_strength=0.7):
    """Render with room layout preservation via Stability AI structure control."""
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/control/structure",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "image/*"},
        files={"image": open(reference_image_path, "rb")},
        data={
            "prompt": prompt,
            "control_strength": control_strength,
            "output_format": "png"
        }
    )
    if response.status_code == 200:
        return response.content  # Raw PNG bytes
    raise Exception(f"Stability API error: {response.status_code} {response.text}")
```

**Flux Depth-Pro via Replicate** (high quality depth control):
```python
import replicate

def render_with_depth_flux(prompt, depth_map_path, control_strength=0.85):
    """Render with depth-controlled Flux via Replicate."""
    output = replicate.run(
        "black-forest-labs/flux-depth-pro",
        input={
            "prompt": prompt,
            "control_image": open(depth_map_path, "rb"),
            "control_strength": control_strength,
            "num_outputs": 1
        }
    )
    return output[0]  # URL to generated image
```

**Stability AI Inpainting** (for masked edits from `/mask-room`):
```python
def render_inpaint(prompt, image_path, mask_path, api_key):
    """Inpaint specific masked region while preserving the rest."""
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "image/*"},
        files={
            "image": open(image_path, "rb"),
            "mask": open(mask_path, "rb")
        },
        data={"prompt": prompt, "output_format": "png"}
    )
    return response.content
```

### Step 3: Output Management
- Save generated images to `output/[style]/[provider]/[timestamp].png`
- Display image paths and metadata
- Log prompt + parameters + provider for reproducibility

### Step 4: Results Summary
Present results:
- Which providers succeeded/failed
- Image file paths
- Cost estimate per generation (if available)
- Suggest `/compare-models` if multiple providers were used
- Suggest `/refine` if the user wants to iterate

## Error Handling
- Missing API key: tell user which env var to set
- Rate limiting: suggest waiting or trying another provider
- Content filtering: adjust prompt and retry
- API errors: show error details and suggest fixes

## Session Relevant Skills

- `/compare-models` — if multiple providers were used, suggest /compare-models to evaluate outputs side-by-side. This is the natural next step after multi-provider rendering.
- `/refine` — if the user is unhappy with the output, /refine takes the prompt + feedback and generates an improved version. Don't manually tweak prompts — /refine tracks iteration history.
- `/generate-prompt` — if no prompt is provided, redirect to /generate-prompt first. Don't accept vague descriptions as render input — proper prompt engineering makes the difference.
- `/edit-design` — if the user wants to modify a rendered result, /edit-design analyzes the output image and generates targeted edit prompts.
- `/style-guide` — reference when troubleshooting style accuracy issues. If renders don't match the expected style, check if the right keywords were used.
- `/preprocess-room` — run this FIRST when working with a reference room photo. It generates depth maps and edge maps that enable layout-controlled rendering.
- `/mask-room` — generates masks for targeted inpainting. Use with the inpainting API calls above.
- `/validate-layout` — run AFTER rendering to verify the generated image preserved the original room layout.

## Gotchas

- **Always save before displaying**: Save images to `output/[style]/[provider]/` before showing results. If the API returns URLs (OpenAI, Grok), download them — URLs expire.
- **Don't render without a proper prompt**: Vague inputs like "make a nice living room" produce poor results. Redirect to /generate-prompt.
- **API keys are per-provider**: Each provider needs its own env var. Check the specific one, don't just say "check your API keys".
- **Gemini image generation model changes frequently**: Verify the current model name in the provider code before calling. Don't hardcode model IDs in prompts.
- **Cost awareness**: DALL-E HD costs ~$0.08/image, Stability ~$0.03, Grok varies. Warn the user before "render all providers".
- **Layout-controlled rendering requires preprocessing first**: Don't skip `/preprocess-room`. Without control maps, you're back to text-only generation which can't guarantee layout preservation.
- **control_strength tuning**: Start at 0.7 for Stability structure, 0.85 for Flux depth. Higher = more layout fidelity but less style freedom. Lower = more creative but may distort room shape.
- **Inpainting needs both image AND mask**: The mask from `/mask-room` defines what changes. White pixels = edit zone, black = preserve.
