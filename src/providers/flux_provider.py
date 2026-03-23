import os

from .base import BaseProvider, RenderResult


class FluxProvider(BaseProvider):
    """Flux image generation provider."""

    def __init__(self) -> None:
        api_key = os.environ.get("FLUX_API_KEY")
        if not api_key:
            raise ValueError("FLUX_API_KEY environment variable is required")
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Flux"

    async def generate(
        self,
        prompt: str,
        *,
        negative_prompt: str | None = None,
        width: int = 1792,
        height: int = 1024,
        num_images: int = 1,
    ) -> list[RenderResult]:
        # Flux API integration — update base URL and model when API becomes available
        results: list[RenderResult] = []
        results.append(
            RenderResult(
                provider=self.name,
                image_path=None,
                image_url=None,
                prompt_used=prompt,
                parameters={"width": width, "height": height},
                success=False,
                error="Flux provider not yet configured — update API endpoint when available",
            )
        )
        return results

    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        return (
            f"A stunning {base_prompt} interior in {style} style. "
            f"Ultra-detailed, 8K resolution, professional interior photography, "
            f"wide-angle lens, photorealistic materials and lighting."
        )
