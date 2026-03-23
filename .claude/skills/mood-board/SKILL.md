---
name: mood-board
description: Generate detailed mood board descriptions with colors, textures, furniture, and lighting for a given interior design style. Use when the user wants to visualize a design concept before rendering.
---

# Mood Board Generator

Create rich, detailed mood board descriptions that capture the essence of a design concept — usable as creative briefs or as input for image generation.

## Input

Gather from user or `$ARGUMENTS`:
- **Design style** (reference `/style-guide`)
- **Room type**
- **Mood/atmosphere**: cozy, dramatic, serene, energetic, luxurious, etc.
- **Any specific elements** to include or avoid

## Mood Board Structure

Generate a comprehensive mood board with these sections:

### 1. Concept Statement
A 2-3 sentence evocative description of the overall design vision. Written in present tense, as if describing a completed space.

### 2. Color Story
- **Dominant color** with hex + description of where it appears
- **Supporting colors** (2-3) with hex + usage
- **Accent pop** with hex + how it creates contrast
- **Overall palette mood**: warm/cool/neutral, saturated/muted

### 3. Texture Map
List 5-7 textures present in the space:
- Surface feel (smooth marble, rough linen, brushed brass)
- Visual texture (pattern, grain, weave)
- How textures create contrast and depth

### 4. Key Furniture Pieces
5-8 specific furniture items:
- Name + style description
- Material and color
- Role in the composition (focal point, supporting, functional)

### 5. Lighting Atmosphere
- Natural light quality (golden hour, overcast, bright noon)
- Artificial lighting mood (warm glow, focused spots, ambient wash)
- Shadow play and highlights

### 6. Decorative Elements
- Artwork style and placement
- Plants/greenery type and arrangement
- Accessories (vases, books, candles, sculptures)
- Textiles (throws, cushions, rugs)

### 7. Sensory Experience
Brief evocative description engaging multiple senses:
- What you see on entering
- Textures you'd want to touch
- Implied sounds (crackling fire, water feature, silence)
- Suggested scents (cedar, fresh linen, jasmine)

## Output Format

Present as a structured document with clear sections. End with:
- Suggested next step: `/generate-prompt [style] [room]` to create AI prompts from this mood board
- Note which elements are most important to capture in the prompt
