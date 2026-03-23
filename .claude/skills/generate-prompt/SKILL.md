---
name: generate-prompt
description: Generate optimized image generation prompts for a specific interior design style and AI provider. Use when the user wants to create prompts for rendering interior designs.
---

# Generate Interior Design Prompt

Create optimized image generation prompts tailored to specific AI providers and design styles.

## Input Requirements

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room type**: living room, bedroom, kitchen, bathroom, office, dining room, etc.
2. **Design style**: reference `/style-guide` for available styles
3. **Target provider**: Gemini, OpenAI/DALL-E, Grok, Stability AI, Midjourney, Flux, or "all"
4. **Additional details** (optional): room dimensions, specific furniture, color preferences, lighting mood, camera angle

## Prompt Structure Per Provider

### OpenAI (DALL-E 3 / GPT-4o)
```
[Room type] interior design in [style] style. [Detailed description of furniture, materials, colors].
Lighting: [lighting type]. Camera angle: [angle]. Photorealistic, 8K, interior photography, architectural digest quality.
```
- Keep under 400 characters for DALL-E 3
- Be explicit about photorealism
- Specify camera angle for composition

### Google Gemini (Imagen)
```
A photorealistic interior photograph of a [room type] designed in [style] style.
Features: [materials], [furniture], [colors], [textures].
Atmosphere: [lighting], [mood].
Style: professional interior photography, high resolution, detailed textures.
```
- Gemini responds well to structured, descriptive prompts
- Emphasize "photograph" for realism

### Stability AI (Stable Diffusion)
```
Positive: photorealistic interior design, [room type], [style] style, [materials], [colors], [furniture], [lighting], professional photography, 8k uhd, ray tracing, detailed textures
Negative: cartoon, drawing, sketch, low quality, blurry, distorted, watermark, text
```
- Always include negative prompt
- Use comma-separated keyword style
- Include quality boosters: 8k, ray tracing, detailed

### Midjourney
```
[Room type] interior, [style] design style, [key materials and colors], [lighting mood], professional interior photography --ar 16:9 --v 6 --style raw --q 2
```
- Use `--ar` for aspect ratio (16:9 for wide rooms, 4:3 for detail shots)
- `--style raw` for photorealism
- Keep descriptive, flowing language

### Grok (xAI)
```
Generate a photorealistic image of a [room type] with [style] interior design.
Include: [specific furniture], [materials like marble/wood/fabric], [color palette].
Mood: [warm/cool/dramatic/serene]. Lighting: [natural/artificial/mixed].
```

### Flux
```
A stunning [room type] interior in [style] style. [Materials] surfaces, [furniture descriptions], [color palette]. [Lighting description]. Shot with a wide-angle lens, professional interior photography, ultra-detailed, 8K resolution.
```

## Output Format

Present the generated prompts in a clear format:
1. Show the prompt for each requested provider
2. Highlight style-specific keywords used (from style guide)
3. Suggest 2-3 variations (different camera angles, lighting moods, or detail focus)
4. Note any provider-specific limitations or tips
