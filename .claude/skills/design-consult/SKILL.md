---
name: design-consult
description: Full AI-powered interior design consultation — room analysis, style recommendation, color palette, materials, and furniture suggestions. Use when the user wants design advice or a complete design brief.
---

# Interior Design Consultation

Provide comprehensive design consultation by analyzing requirements and producing a complete design brief.

## Consultation Flow

### Step 1: Gather Requirements
Ask the user (if not provided via `$ARGUMENTS`):
- **Space**: Room type, approximate dimensions, existing architectural features (windows, columns, ceiling height)
- **Purpose**: Primary use, number of occupants, lifestyle needs (pets, children, work-from-home)
- **Preferences**: Liked styles, colors they're drawn to, any inspirations (photos, references)
- **Constraints**: Budget range (luxury/mid/budget), climate considerations, existing furniture to keep
- **Mood**: Desired atmosphere (cozy, energetic, serene, dramatic, professional)

### Step 2: Style Recommendation
Based on requirements, recommend 2-3 suitable styles with reasoning:
- Primary style recommendation with justification
- Alternative style that addresses the same needs differently
- Optional: fusion/hybrid style combining elements

Reference `/style-guide` for style characteristics.

### Step 3: Color Palette
Generate a cohesive color palette:
- **Primary color** (60% of space): walls, large surfaces
- **Secondary color** (30%): upholstery, curtains, rugs
- **Accent color** (10%): decorative objects, artwork, throws
- Include hex codes and color names
- Consider lighting conditions (natural light direction, artificial lighting)

### Step 4: Materials & Textures
Recommend materials appropriate to the style:
- **Flooring**: type, color, pattern
- **Wall treatments**: paint, wallpaper, paneling, texture
- **Fabrics**: upholstery, curtains, rugs — material and texture
- **Hard surfaces**: countertops, tabletops — material
- **Metals/finishes**: hardware, fixtures, frames

### Step 5: Furniture Layout Concepts
Suggest key furniture pieces:
- Essential pieces for the room type
- Style-appropriate selections with descriptions
- Spatial arrangement principles (focal point, traffic flow, zones)
- Scale guidance relative to room dimensions

### Step 6: Lighting Plan
Recommend lighting layers:
- **Ambient**: general room illumination
- **Task**: functional lighting for activities
- **Accent**: highlighting features, artwork, architecture
- **Decorative**: statement fixtures that serve as design elements
- Color temperature recommendations (warm/neutral/cool)

### Step 7: Design Brief Output
Compile everything into a structured design brief:

```
## Design Brief: [Room Name]
### Style: [Primary Style] (with [Secondary] influences)
### Color Palette: [colors with hex codes]
### Key Materials: [top 5 materials]
### Furniture Plan: [key pieces]
### Lighting: [approach summary]
### Mood: [atmosphere description]
### Next Steps: [suggest using /generate-prompt or /mood-board]
```

After delivering the brief, suggest next actions:
- `/generate-prompt` to create AI rendering prompts based on this brief
- `/mood-board` to generate a visual mood board description
- `/render` to send prompts directly to AI providers
