"""Prompt builder that combines style data with provider-specific optimization."""

from src.providers.registry import get_provider, list_providers
from src.styles.catalog import DesignStyle, get_style


def build_prompt(
    room_type: str,
    style_name: str,
    *,
    provider_name: str | None = None,
    lighting: str = "natural lighting",
    camera_angle: str = "wide-angle",
    extra_details: str = "",
) -> dict[str, str]:
    """Build optimized prompts for one or all providers.

    Returns a dict mapping provider name to optimized prompt string.
    """
    style = get_style(style_name)
    base = _compose_base_prompt(room_type, style, lighting, camera_angle, extra_details)

    if provider_name:
        provider = get_provider(provider_name)
        return {provider.name: provider.optimize_prompt(base, style.name)}

    # Build for all providers
    result: dict[str, str] = {}
    for name in list_providers():
        try:
            provider = get_provider(name)
            result[provider.name] = provider.optimize_prompt(base, style.name)
        except ValueError:
            # Skip providers without API keys configured
            result[name] = f"[{name}: API key not configured]"
    return result


def _compose_base_prompt(
    room_type: str,
    style: DesignStyle,
    lighting: str,
    camera_angle: str,
    extra_details: str,
) -> str:
    """Compose a base prompt from room type and style data."""
    materials = ", ".join(style.materials[:4])
    colors = ", ".join(style.colors[:3])
    keywords = ", ".join(style.keywords[:3])

    parts = [
        room_type,
        f"with {materials}",
        f"in {colors} color palette",
        f"{keywords} atmosphere",
        f"{lighting}",
        f"{camera_angle} shot",
    ]

    if extra_details:
        parts.append(extra_details)

    return ", ".join(parts)
