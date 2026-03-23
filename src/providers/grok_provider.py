import os

from openai import AsyncOpenAI

from .base import BaseProvider, RenderResult


class GrokProvider(BaseProvider):
    """xAI Grok image generation provider (OpenAI-compatible API)."""

    def __init__(self) -> None:
        api_key = os.environ.get("GROK_API_KEY")
        if not api_key:
            raise ValueError("GROK_API_KEY environment variable is required")
        self._client = AsyncOpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    @property
    def name(self) -> str:
        return "xAI Grok"

    async def generate(
        self,
        prompt: str,
        *,
        negative_prompt: str | None = None,
        width: int = 1792,
        height: int = 1024,
        num_images: int = 1,
    ) -> list[RenderResult]:
        results: list[RenderResult] = []

        try:
            response = await self._client.images.generate(
                model="grok-2-image",
                prompt=prompt,
                n=min(num_images, 4),
            )

            for image_data in response.data:
                results.append(
                    RenderResult(
                        provider=self.name,
                        image_path=None,
                        image_url=image_data.url,
                        prompt_used=prompt,
                        parameters={"model": "grok-2-image"},
                        success=True,
                    )
                )
        except Exception as e:
            results.append(
                RenderResult(
                    provider=self.name,
                    image_path=None,
                    image_url=None,
                    prompt_used=prompt,
                    parameters={"model": "grok-2-image"},
                    success=False,
                    error=str(e),
                )
            )

        return results

    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        return (
            f"Generate a photorealistic image of a {base_prompt} with {style} interior design. "
            f"Include detailed materials, realistic lighting, and accurate proportions. "
            f"Professional interior photography quality."
        )
