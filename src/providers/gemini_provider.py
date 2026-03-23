import os

from .base import BaseProvider, RenderResult


class GeminiProvider(BaseProvider):
    """Google Gemini image generation provider."""

    def __init__(self) -> None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Google Gemini"

    async def generate(
        self,
        prompt: str,
        *,
        negative_prompt: str | None = None,
        width: int = 1792,
        height: int = 1024,
        num_images: int = 1,
    ) -> list[RenderResult]:
        import google.generativeai as genai

        genai.configure(api_key=self._api_key)

        results: list[RenderResult] = []
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            await model.generate_content_async(prompt)

            results.append(
                RenderResult(
                    provider=self.name,
                    image_path=None,
                    image_url=None,
                    prompt_used=prompt,
                    parameters={"model": "gemini-2.0-flash-exp"},
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
                    parameters={"model": "gemini-2.0-flash-exp"},
                    success=False,
                    error=str(e),
                )
            )

        return results

    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        return (
            f"A photorealistic interior photograph of a {base_prompt} designed in {style} style. "
            f"Professional interior photography, high resolution, detailed textures, "
            f"natural lighting, architectural magazine quality."
        )
