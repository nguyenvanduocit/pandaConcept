import os
import tempfile

from .base import BaseProvider, RenderResult


class GeminiProvider(BaseProvider):
    """Google Gemini image generation provider using google.genai SDK."""

    MODEL = "gemini-3.1-flash-image-preview"

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
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self._api_key)

        results: list[RenderResult] = []
        try:
            response = client.models.generate_content(
                model=self.MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

            image_path = None
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    mime = part.inline_data.mime_type
                    ext = "png" if "png" in mime else "jpg"
                    fd, image_path = tempfile.mkstemp(suffix=f".{ext}")
                    with os.fdopen(fd, "wb") as f:
                        f.write(part.inline_data.data)
                    break

            results.append(
                RenderResult(
                    provider=self.name,
                    image_path=image_path,
                    image_url=None,
                    prompt_used=prompt,
                    parameters={"model": self.MODEL},
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
                    parameters={"model": self.MODEL},
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
