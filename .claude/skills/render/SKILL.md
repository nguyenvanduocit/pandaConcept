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
