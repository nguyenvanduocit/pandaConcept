---
name: compare-models
description: Side-by-side comparison of image generation outputs across different AI providers. Use after rendering the same prompt through multiple providers to evaluate quality, style accuracy, and cost.
---

# Compare AI Model Outputs

Analyze and compare interior design renders from different AI providers to help the user choose the best output or provider for their needs.

## Input

- Multiple rendered images from `/render` (or image paths provided by user)
- The original prompt used
- The target design style

## Comparison Criteria

Evaluate each provider's output on:

### 1. Style Accuracy
- Does it match the requested interior design style?
- Are style-specific materials, colors, and furniture correct?
- Rate: Excellent / Good / Partial / Poor

### 2. Photorealism
- Does it look like a real photograph?
- Texture quality and material rendering
- Lighting naturalness
- Rate: Photorealistic / Near-photo / Illustrated / Artificial

### 3. Composition
- Camera angle and framing
- Spatial depth and perspective accuracy
- Room proportions and scale of furniture
- Rate: Professional / Adequate / Awkward

### 4. Detail Quality
- Fine details: fabric patterns, wood grain, reflections
- Consistency: no floating objects, impossible geometry, weird artifacts
- Text/watermark issues
- Rate: High detail / Medium / Low / Artifacts present

### 5. Color Fidelity
- Does the color palette match the design brief?
- Color harmony and balance
- Lighting effect on colors (warm/cool cast)

### 6. Practical Value
- Could this image be used in a client presentation?
- Would it work as a design reference?
- Does it communicate the design intent clearly?

## Output Format

```
## Model Comparison: [Style] [Room]

| Criteria         | Gemini | OpenAI | Stability | Grok | Flux |
|-----------------|--------|--------|-----------|------|------|
| Style Accuracy  |   ★★★  |  ★★★★  |   ★★★★    | ★★★  | ★★★★ |
| Photorealism    |   ...  |  ...   |   ...     | ...  | ...  |
| Composition     |   ...  |  ...   |   ...     | ...  | ...  |
| Detail Quality  |   ...  |  ...   |   ...     | ...  | ...  |
| Color Fidelity  |   ...  |  ...   |   ...     | ...  | ...  |

### Best For:
- **Client presentation**: [provider] — [reason]
- **Design exploration**: [provider] — [reason]
- **Quick iteration**: [provider] — [reason]
- **Budget-conscious**: [provider] — [reason]

### Recommendations:
- [Specific refinement suggestions per provider]
```

Suggest `/refine` for the most promising output to iterate further.
