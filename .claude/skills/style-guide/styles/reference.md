# PART 4: MASTER AI RENDERING REFERENCE

---

## Style Keyword Matrix

| Style | Primary Keywords | Mood Keywords | Light Keywords |
|---|---|---|---|
| Japanese Minimalism | tatami, shoji, tokonoma, ma, zabuton | serene, zen, contemplative | diffused, soft, directional |
| Scandinavian | birch, hygge, PH lamp, lagom | cozy, functional, light | maximized natural, candlelight |
| Warm Minimalism | limewash, travertine, bouclé, brass | warm, curated, restrained | ambient, warm-toned |
| Japandi | shou sugi ban, washi, linen, live-edge oak | harmonious, natural, minimal | washi filtered, cove |
| Contemporary | bouclé, travertine, arched, fluted | current, warm, organic | sculptural, layered |
| Bauhaus | tubular steel, primary color, geometric | functional, rational, bold | industrial track, glass |
| Mediterranean (Greek) | cycladic white, aegean blue, mosaic | sun-kissed, timeless, warm | strong directional, shadowed |
| Mediterranean (Italian) | Murano, travertine, fresco, brocade | opulent, historic, warm | dramatic chandelier |
| Mediterranean (Spanish) | azulejo, moorish arch, terracotta | vibrant, cultural, textured | dappled courtyard |
| Tropical | rattan, bamboo, botanical print, teak | lush, relaxed, open | filtered jungle, open sky |
| Coastal/Hamptons | shiplap, linen, navy, sisal | relaxed luxury, breezy | washed, ocean-bright |
| Rustic | log beam, stone fireplace, cowhide | rugged, warm, authentic | amber firelight |
| Farmhouse | shiplap, apron sink, barn door, sage | homey, practical, warm | natural, industrial pendant |
| Desert/Southwestern | adobe, vigas, saltillo, kiva, turquoise | earthy, cultural, warm | desert sun, candlelight |
| Industrial | exposed brick, concrete, matte black | raw, urban, honest | Edison filament, industrial |
| Brutalist | raw concrete, geometric, cantilevered | austere, monumental, bold | light shafts, dramatic |
| Biophilic | living wall, skylight, natural stone, moss | restorative, connected, calm | full-spectrum, circadian |
| Maximalist | jewel tones, velvet, pattern mix, gallery | bold, personal, joyful | sculptural chandelier |
| Retro/Vintage | era-specific objects, pattern, decade color | nostalgic, playful, expressive | warm, lamp-lit |
| Futuristic/Sci-Fi | parametric, LED, smart glass, polished | innovative, clean, intelligent | LED architectural |
| Bohemian | rattan, macramé, kilim, layered | free-spirited, global, warm | candlelight, lantern |
| Wabi-Kintsugi | kintsugi, weathered, imperfect, patina | contemplative, accepting, quiet | natural variable, single point |

---

## Universal AI Prompt Formula

```
[STYLE] interior design, [ROOM TYPE], [DOMINANT MATERIAL], [COLOR PALETTE],
[LIGHTING TYPE], [FURNITURE DESCRIPTION], [ARCHITECTURAL FEATURE],
[ATMOSPHERE/MOOD], [SEASON/TIME OF DAY], photorealistic, 4K, editorial photography,
[CAMERA ANGLE], [NEGATIVE PROMPT]
```

### Example Prompts by Style

**Japanese Minimalism Living Room:**
```
Japanese minimalist living room, ma negative space, hinoki wood floor, shoji screen diffused light,
washi paper pendant single hanging, low zabuton floor cushion, tokonoma alcove with single ceramic,
pale persimmon accent, serene contemplative mood, morning light, photorealistic 4K architectural
photography, wide-angle eye level, --no clutter, bright colors, Western furniture, ceiling fixtures
```

**Japandi Bedroom:**
```
Japandi bedroom interior, platform bed smoked cedar frame, 100% linen bedding oyster white,
live-edge oak floating shelf, bamboo screen beside window, single orchid ikebana, warm ambient cove lighting,
warm sand and charcoal palette, serene harmonious atmosphere, dawn light, photorealistic 4K,
interior design photography, eye-level angle, --no pattern, bright colors, plastic elements
```

**Mediterranean Kitchen (Italian):**
```
Italian Mediterranean kitchen, Carrara marble countertop, hand-painted majolica tile backsplash,
dark walnut open shelving, terracotta floor tile, Tuscan ochre walls, Murano glass pendant,
iron pot rack ceiling mounted, ornate carved cabinet detail, warm golden light, early afternoon sun,
4K photorealistic, editorial interior photography, eye-level slight upward, --no modern appliances visible,
cold light, white cabinetry
```

**Industrial NYC Loft:**
```
NYC industrial loft interior, exposed red brick wall, polished concrete floor, crittal steel window
wall double height, aged leather chesterfield sofa, reclaimed timber dining table steel trestle legs,
Edison filament pendant cluster conduit, matte black pipe shelving, exposed steel beam ceiling,
evening warm industrial lighting, urban street view beyond glass, 4K photorealistic, wide-angle architectural,
--no soft curtains, pastel colors, suburban furniture
```

**Biophilic Living Room:**
```
Biophilic living room, floor-to-ceiling operable glass wall to garden, living moss wall panel,
monstera deliciosa large specimen, live-edge walnut shelf, rammed earth feature wall, cork floor,
jute rug, natural linen sofa organic form, full-spectrum skylight, morning warm light,
forest floor green sage mushroom palette, restorative calm atmosphere, 4K interior design photography,
wide-angle, --no synthetic materials, dead plants, artificial flowers
```

---

## Provider-Specific Notes

### Midjourney
- Add `--ar 16:9` for wide-angle room shots; `--ar 4:5` for portrait orientation
- Use `--style raw` for photorealistic interiors
- Add `--v 6` for 2025 quality level
- Use `::weight` modifiers to emphasize critical elements
- Negative prompts via `--no`

### DALL-E 3 (GPT-4o)
- Write in descriptive sentences, not keyword lists
- Include camera angle and focal length description
- Add "editorial interior design photography" for photorealistic output
- Include time of day and lighting description explicitly

### Stable Diffusion / SDXL
- Use style LoRA models for period-specific accuracy
- Add negative prompts as dedicated field
- CFG scale 7–9 for photorealistic
- Add "realistic, 8K, hyperrealistic, architectural visualization" for quality boost

### Gemini
- Explicitly describe material textures ("rough-sawn timber with visible grain")
- Include emotional/atmospheric language ("creates feeling of sheltered warmth")
- Reference specific designer or brand references for style precision

### Flux
- Detailed material and color specifications most effective
- Include specific object placement ("centered on left wall, beside window")
- Architectural drawings reference for complex spaces

---

## Style Compatibility Matrix

| Style | Works Well With | Avoid Mixing With |
|---|---|---|
| Japanese Minimalism | Japandi, Scandinavian, Biophilic, Wabi-Sabi | Maximalist, Baroque, Retro |
| Scandinavian | Japandi, Farmhouse, Coastal, Contemporary | Heavy Mediterranean, Baroque |
| Japandi | Japanese Min, Scandinavian, Biophilic, Wabi-Sabi | Industrial (unless Soft), Maximalist |
| Contemporary | Most styles (transitional nature) | Hard Brutalist, Retro pastiche |
| Bauhaus | Industrial, Brutalist, MCM | Bohemian, Baroque, Rustic |
| Mediterranean | Bohemian, Rustic, Maximalist | Industrial, Brutalist, Futuristic |
| Tropical | Bohemian, Biophilic, Coastal | Brutalist, Futuristic |
| Coastal/Hamptons | Scandinavian, Farmhouse, Contemporary | Industrial, Brutalist |
| Industrial | Bauhaus, Brutalist, Rustic (selective) | Tropical, Bohemian |
| Biophilic | All styles (layerable philosophy) | None — enhances any style |
| Maximalist | Bohemian, MCM, Mediterranean, Retro | Minimalist (tension) |
| Bohemian | Maximalist, Rustic, Tropical, Mediterranean | Bauhaus, Brutalist |
| Wabi-Sabi | Japandi, Japanese Min, Biophilic, Contemporary | Maximalist, Retro, Futuristic |

---

## Material Glossary

| Material | Origin/Context | Styles |
|---|---|---|
| Bouclé | Looped yarn fabric, French textile | Contemporary, Warm Min, Japandi |
| Travertine | Limestone with voids, Italian quarry | Contemporary, Mediterranean, Warm Min |
| Shiplap | Overlapping plank wall cladding | Farmhouse, Coastal |
| Shou Sugi Ban | Japanese charred cedar (*Yakisugi*) | Japandi, Wabi-Sabi |
| Washi | Japanese handmade paper, mulberry fiber | Japanese Min, Japandi |
| Zellige | Moroccan hand-chiseled ceramic mosaic tile | Mediterranean, Bohemian, Maximalist |
| Saltillo | Mexican sun-dried unglazed terracotta tile | Desert SW, Mediterranean |
| Tatami | Woven rice straw mat (Japanese standard module) | Japanese Minimalism |
| Kilim | Flat-weave Turkish/Moroccan rug | Bohemian, Rustic, Maximalist |
| Limewash | Calcium hydroxide paint, depth and texture | Warm Min, Contemporary, Farmhouse |
| Encaustic | Cement pigment pressed tile, patterned | Mediterranean, Farmhouse, Bohemian |
| Rattan | Palm vine, core and peel | Tropical, Coastal, Bohemian, Japandi |
| Abaca | Manila hemp plant fiber | Tropical, Biophilic |
| Jesmonite | Acrylic-mineral composite (casting) | Contemporary, Futuristic |
| Kintsugi | Gold lacquer ceramic repair (urushi + gold) | Wabi-Sabi philosophy |
| Vigas | Peeled log ceiling beams (Southwestern) | Desert SW |
| Azulejo | Hand-painted Portuguese/Spanish ceramic tile | Mediterranean Spanish |
| Bizen ware | Unglazed Japanese stoneware, kiln-fired | Japanese Min, Wabi-Sabi |
| Tapa cloth | Polynesian bark cloth, Pacific islands | Tropical/Hawaiian |
| Sashiko | Japanese geometric running-stitch embroidery | Japanese Min, Japandi |

---

## Room-Specific Material Decisions

### Kitchen
| Style | Countertop | Floor | Cabinetry | Backsplash |
|---|---|---|---|---|
| Japandi | Concrete / Soapstone | Wide-plank oak | Handleless smoked oak | Stone slab |
| Mediterranean | Carrara marble | Saltillo tile | Dark walnut | Majolica tile |
| Farmhouse | Soapstone / Quartz | Wire-brushed oak | White painted | Subway tile |
| Industrial | Zinc / Steel | Polished concrete | Open steel shelving | Brick |
| Contemporary | Travertine (unfilled) | Terrazzo | Fluted oak | Slab stone |
| Maximalist | Marble (dramatic vein) | Encaustic tile | Lacquered jewel | Zellige mosaic |

### Bathroom
| Style | Floor | Walls | Vanity Top | Fixtures |
|---|---|---|---|---|
| Japanese Min | River pebble / Hinoki slatted | Plaster / Washi | Teak bench | Matte black |
| Scandinavian | White hexagonal tile | White subway | Marble slab | Chrome |
| Contemporary | Large travertine slab | Limewash plaster | Travertine | Unlacquered brass |
| Industrial | Polished concrete | Exposed brick | Zinc / Concrete | Black iron |
| Tropical | Pebble mosaic | Outdoor stone | Teak | Brushed nickel |
| Brutalist | Poured concrete | Board-form concrete | Concrete trough | Matte black |

---

## Color Hex Reference by Category

### Whites & Neutrals
- Arctic White: `#F7F5F2` (Scandinavian)
- Farmhouse White: `#F2EEE8` (Farmhouse)
- Washi White: `#F0EAE0` (Wabi-Sabi)
- Kinari Cream: `#EDE0C4` (Japandi)
- Limewash Cream: `#EDE5D0` (Warm Minimalism)
- Warm Sand: `#C8B89A` (Warm Minimalism)
- Nordic Snow: `#FAFAF8` (Scandinavian)
- Warm Oat: `#E8D9C0` (Scandinavian)
- Polar White: `#F5F5F5` (Futuristic)
- Cycladic White: `#F4F1EC` (Greek Mediterranean)
- Frangipani White: `#F5F0E8` (Tropical)
- Hamptons White: `#F5F3EE` (Coastal)

### Earthy Reds & Terracottas
- Tuscan Terracotta: `#B05C35` (Italian Mediterranean)
- Burnt Sienna: `#8B3A20` (Desert SW)
- Adobe Clay: `#C07850` (Desert SW)
- Terracotta: `#B06A40` (Bohemian)
- Rust Red: `#8B3A20` (Rustic)
- Warm Terracotta: `#C4714A` (Contemporary)
- Brick Red: `#8B3A28` (Industrial)
- Adobe: `#C08050` (Spanish Mediterranean)
- Corten Orange: `#8B4A20` (Brutalist)

### Greens
- Forest Floor: `#4A5A38` (Biophilic)
- Lichen Green: `#8FA882` (Scandinavian)
- Jungle Green: `#2D5A2D` (Tropical)
- Sage Cactus: `#6A8A5A` (Desert SW)
- Olive: `#6A7A3A` (Bohemian)
- Norwegian Forest: `#3D5A40` (Scandinavian)
- Moss Green: `#5A7A4A` (Biophilic)
- Sage Green: `#7A9070` (Farmhouse)
- Olive Green: `#6B7C45` (Contemporary)
- Forest Green: `#2D5A3D` (Neo-Bauhaus / Italian Mediterranean)
- Forest Green (Soft Industrial): `#3A5A3A` (Industrial)

### Blues
- Aegean Blue: `#1A5276` (Greek Mediterranean)
- Moorish Blue: `#2A5B8C` (Spanish Mediterranean)
- Navy Stripe: `#1A3A5C` (Coastal)
- Midnight Blue: `#2E3D5C` (Scandinavian)
- Cobalt Sky: `#2E86C1` (Greek Mediterranean)
- Deep Teal: `#2A5C6A` (Contemporary)
- Neon Blue: `#2060E8` (Futuristic)
- Swedish Blue: `#5B7FA6` (Scandinavian)
- Cobalt (2025 Pop): `#1E3F8C` (Contemporary)
- Primary Blue: `#1A3A8C` (Bauhaus)

### Metallics
- Aged Brass: `#A0784A` (Warm Minimalism)
- Kintsugi Gold: `#C8902A` (Wabi-Sabi)
- Bauhaus Yellow: `#F0C020` (Bauhaus — primary)
- Chrome Silver: `#C0C0C0` (Futuristic)
- Venetian Gold: `#C8A44A` (Italian Mediterranean)
- Gold: `#C8A020` (Maximalist)
- Aged Copper: `#8B5A3A` (Industrial)
- Rose Gold: `#C0706A` (Futuristic warm)

### Bold / Jewel
- Emerald Green: `#1A5C3A` (Maximalist)
- Sapphire Blue: `#1A3A8C` (Maximalist)
- Deep Wine: `#6A1A2A` (Maximalist 2025)
- Turquoise: `#2A8A8A` (Desert SW signature)
- Electric Purple: `#6020C0` (Futuristic)
- Fuchsia: `#C8208A` (Maximalist)
- Primary Red: `#CC2020` (Bauhaus)
- Neon Fuchsia: `#E8208A` (1980s Retro)

---

*Condensed from: 2026-03-23 Research Report*
*Styles: 20 primary (with 30+ sub-variations)*
*Purpose: pandaConcept AI interior design image generation*
