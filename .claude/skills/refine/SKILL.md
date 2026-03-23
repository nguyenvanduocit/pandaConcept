---
name: refine
description: Iteratively refine image generation prompts based on feedback about previous renders. Use when the user wants to improve a generated interior design image.
---

# Iterative Prompt Refinement

Improve interior design renders through systematic prompt refinement based on user feedback.

## Input

Gather from user or `$ARGUMENTS`:
- **Previous prompt**: the prompt that generated the current image
- **Provider**: which AI provider was used
- **Feedback**: what to improve (can be free-form)
- **Reference image path** (optional): the current render to improve upon

## Refinement Categories

Guide the user through specific feedback if their input is vague:

### Style Adjustments
- "More/less [style element]" — adjust style keyword intensity
- "Add [style] influences" — blend in secondary style elements
- "Wrong period/era" — correct historical references

### Color Corrections
- "Too warm/cool" — adjust color temperature keywords
- "More contrast/muted" — modify saturation descriptors
- "Wrong dominant color" — restructure color priority in prompt

### Composition Changes
- "Different angle" — modify camera/perspective keywords
- "Closer/wider view" — adjust focal length descriptors
- "Show more of [area]" — reframe composition focus

### Detail Improvements
- "More texture detail" — add specific material descriptors
- "Furniture looks wrong" — specify exact furniture styles
- "Lighting is off" — adjust lighting keywords (golden hour, diffused, dramatic)

### Realism Boost
- "Looks too AI-generated" — add photography-specific terms
- "Proportions are off" — add scale references
- "Missing shadows/reflections" — add rendering quality keywords

## Refinement Process

1. **Analyze feedback** against the original prompt
2. **Identify weak areas** in the prompt that caused the issue
3. **Generate refined prompt** with tracked changes (show diff)
4. **Explain changes**: why each modification should improve the result
5. **Suggest provider switch** if the issue is provider-specific (e.g., "Stability handles textures better for this style")

## Output

```
### Original Prompt:
[original]

### Feedback Applied:
- [change 1]: [reason]
- [change 2]: [reason]

### Refined Prompt:
[new prompt]

### Expected Improvement:
[what should be different in the new render]
```

Offer to `/render` the refined prompt immediately, or generate additional variations.

## Refinement History

Track refinement iterations so the user can see progression:
- Iteration 1: original prompt
- Iteration 2: [feedback] → [changes]
- Iteration 3: [feedback] → [changes]

This history helps identify patterns in what works for specific styles and providers.
