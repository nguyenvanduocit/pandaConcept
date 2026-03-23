import os

from openai import AsyncOpenAI

from .base import BaseProvider, RenderResult


class OpenAIProvider(BaseProvider):
    """OpenAI DALL-E 3 / GPT-4o image generation provider."""

    def __init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self._client = AsyncOpenAI(api_key=api_key)

    @property
    def name(self) -> str:
        return "OpenAI (DALL-E 3)"

    async def generate(
        self,
        prompt: str,
        *,
        negative_prompt: str | None = None,
        width: int = 1792,
        height: int = 1024,
        num_images: int = 1,
    ) -> list[RenderResult]:
        size = self._resolve_size(width, height)
        results: list[RenderResult] = []

        try:
            response = await self._client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd",
                n=1,  # DALL-E 3 only supports n=1
            )

            for image_data in response.data:
                results.append(
                    RenderResult(
                        provider=self.name,
                        image_path=None,
                        image_url=image_data.url,
                        prompt_used=prompt,
                        parameters={"model": "dall-e-3", "size": size, "quality": "hd"},
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
                    parameters={"model": "dall-e-3", "size": size},
                    success=False,
                    error=str(e),
                )
            )

        return results

    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        return (
            f"{base_prompt} Interior design in {style} style. "
            f"Photorealistic, 8K, interior photography, architectural digest quality, "
            f"professional lighting, detailed textures and materials."
        )

    @staticmethod
    def _resolve_size(width: int, height: int) -> str:
        """Map dimensions to DALL-E 3 supported sizes."""
        if width > height:
            return "1792x1024"
        elif height > width:
            return "1024x1792"
        else:
            return "1024x1024"
