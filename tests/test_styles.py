from src.styles.catalog import get_style, list_styles, styles_by_category


def test_list_styles_returns_all():
    styles = list_styles()
    assert len(styles) >= 20
    assert "modern" in styles
    assert "japandi" in styles
    assert "vietnamese" in styles


def test_get_style_valid():
    style = get_style("art-deco")
    assert style.name == "Art Deco"
    assert style.category == "Classic & Traditional"
    assert len(style.keywords) > 0
    assert len(style.materials) > 0
    assert len(style.colors) > 0


def test_get_style_invalid():
    try:
        get_style("nonexistent-style")
        raise AssertionError("Should have raised KeyError")
    except KeyError:
        pass


def test_styles_by_category():
    categories = styles_by_category()
    assert "Modern & Contemporary" in categories
    assert "Classic & Traditional" in categories
    assert "Asian & Eastern" in categories
    assert "Regional & Vernacular" in categories
    assert "Specialty & Avant-Garde" in categories


def test_style_has_color_hexes():
    style = get_style("art-deco")
    assert len(style.color_hexes) > 0
    assert "gold" in style.color_hexes
