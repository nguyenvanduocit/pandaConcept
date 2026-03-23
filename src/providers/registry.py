from .base import BaseProvider
from .flux_provider import FluxProvider
from .gemini_provider import GeminiProvider
from .grok_provider import GrokProvider
from .openai_provider import OpenAIProvider
from .stability_provider import StabilityProvider

PROVIDERS: dict[str, type[BaseProvider]] = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "grok": GrokProvider,
    "stability": StabilityProvider,
    "flux": FluxProvider,
}


def get_provider(name: str) -> BaseProvider:
    """Get a provider instance by name. Raises KeyError if unknown."""
    provider_cls = PROVIDERS.get(name.lower())
    if provider_cls is None:
        available = ", ".join(sorted(PROVIDERS.keys()))
        raise KeyError(f"Unknown provider '{name}'. Available: {available}")
    return provider_cls()


def list_providers() -> list[str]:
    """Return sorted list of available provider names."""
    return sorted(PROVIDERS.keys())
