"""Interior design style catalog with characteristics, keywords, and palettes."""

from dataclasses import dataclass, field


@dataclass
class DesignStyle:
    name: str
    category: str
    description: str
    keywords: list[str]
    materials: list[str]
    colors: list[str]
    color_hexes: dict[str, str] = field(default_factory=dict)


STYLES: dict[str, DesignStyle] = {
    "modern": DesignStyle(
        name="Modern",
        category="Modern & Contemporary",
        description="Clean lines, open spaces, neutral palette with bold accents",
        keywords=["sleek", "functional", "uncluttered", "geometric", "open-plan"],
        materials=["glass", "steel", "concrete", "leather", "lacquer"],
        colors=["white", "grey", "black", "bold accent"],
        color_hexes={"white": "#FFFFFF", "grey": "#9E9E9E", "black": "#212121"},
    ),
    "minimalist": DesignStyle(
        name="Minimalist",
        category="Modern & Contemporary",
        description="Less is more — monochromatic, essential furniture only",
        keywords=["sparse", "intentional", "breathing room", "clean", "essential"],
        materials=["natural wood", "white surfaces", "concrete", "linen"],
        colors=["white", "off-white", "light grey", "natural wood"],
        color_hexes={"white": "#FAFAFA", "off-white": "#F5F0EB", "light grey": "#E0E0E0"},
    ),
    "scandinavian": DesignStyle(
        name="Scandinavian",
        category="Modern & Contemporary",
        description="Light woods, white walls, hygge warmth",
        keywords=["cozy", "functional", "light", "hygge", "natural"],
        materials=["birch", "pine", "wool", "linen", "ceramic"],
        colors=["white", "grey", "soft pastels", "natural wood"],
        color_hexes={"white": "#FFFFFF", "soft blue": "#B3CDE0", "blush": "#F4C2C2"},
    ),
    "contemporary": DesignStyle(
        name="Contemporary",
        category="Modern & Contemporary",
        description="Current trends, fluid, eclectic mix",
        keywords=["trending", "curated", "evolving", "fluid", "textured"],
        materials=["mixed metals", "textured fabrics", "glass", "stone"],
        colors=["neutral base", "muted tones", "single bold accent"],
        color_hexes={"charcoal": "#36454F", "taupe": "#B38B6D", "sage": "#9CAF88"},
    ),
    "japandi": DesignStyle(
        name="Japandi",
        category="Modern & Contemporary",
        description="Japanese minimalism meets Scandinavian warmth",
        keywords=["wabi-sabi", "hygge", "harmony", "imperfection", "calm"],
        materials=["light wood", "ceramics", "linen", "bamboo", "stone"],
        colors=["earth tones", "muted greens", "warm white", "charcoal"],
        color_hexes={"warm white": "#FAF6F0", "sage": "#9CAF88", "charcoal": "#36454F"},
    ),
    "mid-century-modern": DesignStyle(
        name="Mid-Century Modern",
        category="Modern & Contemporary",
        description="1950s-60s organic forms, tapered legs, bold colors",
        keywords=["retro-modern", "organic curves", "iconic", "tapered legs"],
        materials=["teak", "walnut", "molded plastic", "brass", "leather"],
        colors=["mustard", "teal", "orange", "olive", "warm wood"],
        color_hexes={"mustard": "#FFDB58", "teal": "#008080", "olive": "#808000"},
    ),
    "neoclassical": DesignStyle(
        name="Neoclassical",
        category="Classic & Traditional",
        description="Greek/Roman symmetry, columns, ornate moldings",
        keywords=["grandeur", "symmetry", "refined", "classical", "elegant"],
        materials=["marble", "gilded accents", "silk", "crystal", "carved wood"],
        colors=["cream", "gold", "navy", "ivory", "pale blue"],
        color_hexes={"cream": "#FFFDD0", "gold": "#D4AF37", "navy": "#000080"},
    ),
    "victorian": DesignStyle(
        name="Victorian",
        category="Classic & Traditional",
        description="Ornate detailing, rich fabrics, dark woods",
        keywords=["elaborate", "layered", "opulent", "ornate", "romantic"],
        materials=["mahogany", "velvet", "brocade", "stained glass", "brass"],
        colors=["deep burgundy", "forest green", "gold", "plum"],
        color_hexes={"burgundy": "#800020", "forest green": "#228B22", "gold": "#FFD700"},
    ),
    "art-deco": DesignStyle(
        name="Art Deco",
        category="Classic & Traditional",
        description="1920s geometric glamour, bold patterns, luxurious materials",
        keywords=["geometric", "luxurious", "dramatic", "glamorous", "bold"],
        materials=["lacquer", "chrome", "exotic woods", "mirror", "velvet"],
        colors=["black", "gold", "emerald", "cobalt", "cream"],
        color_hexes={"black": "#000000", "gold": "#D4AF37", "emerald": "#50C878"},
    ),
    "french-provincial": DesignStyle(
        name="French Provincial",
        category="Classic & Traditional",
        description="Rustic elegance, curved furniture, pastoral charm",
        keywords=["romantic", "pastoral", "charming", "elegant-rustic"],
        materials=["distressed wood", "linen", "wrought iron", "toile", "stone"],
        colors=["soft blue", "lavender", "cream", "sage", "butter yellow"],
        color_hexes={"soft blue": "#A4C8E1", "lavender": "#E6E6FA", "cream": "#FFFDD0"},
    ),
    "japanese": DesignStyle(
        name="Japanese (Wabi-Sabi)",
        category="Asian & Eastern",
        description="Beauty in imperfection, natural materials, zen tranquility",
        keywords=["zen", "asymmetry", "nature", "tranquil", "ma (space)"],
        materials=["bamboo", "rice paper", "natural stone", "tatami", "cedar"],
        colors=["earth tones", "moss green", "warm beige", "charcoal"],
        color_hexes={"moss": "#8A9A5B", "warm beige": "#D2B48C", "charcoal": "#36454F"},
    ),
    "chinese-traditional": DesignStyle(
        name="Chinese Traditional",
        category="Asian & Eastern",
        description="Red and gold symbolism, intricate carvings, feng shui balance",
        keywords=["auspicious", "symbolic", "harmony", "feng shui", "ornate"],
        materials=["lacquered wood", "silk", "jade", "porcelain", "rosewood"],
        colors=["red", "gold", "black", "jade green"],
        color_hexes={"red": "#CC0000", "gold": "#FFD700", "jade": "#00A86B"},
    ),
    "vietnamese": DesignStyle(
        name="Vietnamese",
        category="Asian & Eastern",
        description="Tropical elegance with French-colonial influences",
        keywords=["tropical", "handcraft", "heritage", "natural", "airy"],
        materials=["bamboo", "rattan", "ceramic", "laterite", "teak"],
        colors=["earth tones", "terracotta", "jade green", "warm wood"],
        color_hexes={"terracotta": "#E2725B", "jade": "#00A86B", "teak": "#B5651D"},
    ),
    "indochine": DesignStyle(
        name="Indochine",
        category="Asian & Eastern",
        description="French-Asian fusion, colonial tropical luxury",
        keywords=["colonial-tropical", "fusion", "lush", "exotic", "layered"],
        materials=["dark wood", "rattan", "silk", "brass", "ceramic tile"],
        colors=["emerald", "amber", "cream", "dark wood tones"],
        color_hexes={"emerald": "#50C878", "amber": "#FFBF00", "cream": "#FFFDD0"},
    ),
    "mediterranean": DesignStyle(
        name="Mediterranean",
        category="Regional & Vernacular",
        description="Sun-washed warmth, terracotta, rustic coastal charm",
        keywords=["coastal", "warm", "textured", "arched", "sun-drenched"],
        materials=["stucco", "terracotta tile", "wrought iron", "natural stone"],
        colors=["blue", "white", "terracotta", "olive green"],
        color_hexes={"blue": "#1E90FF", "terracotta": "#E2725B", "olive": "#808000"},
    ),
    "tropical": DesignStyle(
        name="Tropical",
        category="Regional & Vernacular",
        description="Indoor-outdoor living, lush greenery, natural breezes",
        keywords=["paradise", "natural", "breezy", "lush", "resort"],
        materials=["rattan", "teak", "palm", "bamboo", "linen"],
        colors=["green", "turquoise", "coral", "natural wood"],
        color_hexes={"green": "#2E8B57", "turquoise": "#40E0D0", "coral": "#FF7F50"},
    ),
    "bohemian": DesignStyle(
        name="Bohemian",
        category="Regional & Vernacular",
        description="Eclectic, globally collected, layered textures",
        keywords=["free-spirited", "layered", "collected", "eclectic", "handmade"],
        materials=["mixed textiles", "macramé", "vintage furniture", "kilim", "rattan"],
        colors=["jewel tones", "warm earth", "mustard", "terracotta", "teal"],
        color_hexes={"mustard": "#FFDB58", "terracotta": "#E2725B", "teal": "#008080"},
    ),
    "industrial": DesignStyle(
        name="Industrial",
        category="Specialty & Avant-Garde",
        description="Exposed structure, raw materials, urban loft aesthetic",
        keywords=["urban", "raw", "utilitarian", "exposed", "loft"],
        materials=["exposed brick", "steel", "concrete", "reclaimed wood", "iron pipe"],
        colors=["grey", "black", "rust", "warm wood accents"],
        color_hexes={"grey": "#808080", "rust": "#B7410E", "black": "#1A1A1A"},
    ),
    "biophilic": DesignStyle(
        name="Biophilic",
        category="Specialty & Avant-Garde",
        description="Deep nature integration, living walls, wellness-focused",
        keywords=["nature-connected", "wellness", "organic", "living", "green"],
        materials=["living plants", "natural wood", "stone", "water features", "cork"],
        colors=["greens", "earth tones", "natural wood", "sky blue"],
        color_hexes={"leaf green": "#4CAF50", "earth": "#8B7355", "sky": "#87CEEB"},
    ),
    "futuristic": DesignStyle(
        name="Futuristic",
        category="Specialty & Avant-Garde",
        description="Cutting-edge tech integration, sleek minimalism",
        keywords=["high-tech", "streamlined", "innovative", "smart-home", "luminous"],
        materials=["acrylic", "LED panels", "smart glass", "carbon fiber", "resin"],
        colors=["white", "silver", "neon accents", "holographic"],
        color_hexes={"white": "#F8F8FF", "silver": "#C0C0C0", "neon blue": "#00F0FF"},
    ),
}


def get_style(name: str) -> DesignStyle:
    """Get a design style by key. Raises KeyError if unknown."""
    key = name.lower().replace(" ", "-")
    style = STYLES.get(key)
    if style is None:
        available = ", ".join(sorted(STYLES.keys()))
        raise KeyError(f"Unknown style '{name}'. Available: {available}")
    return style


def list_styles() -> list[str]:
    """Return sorted list of available style keys."""
    return sorted(STYLES.keys())


def styles_by_category() -> dict[str, list[DesignStyle]]:
    """Group styles by category."""
    categories: dict[str, list[DesignStyle]] = {}
    for style in STYLES.values():
        categories.setdefault(style.category, []).append(style)
    return categories
