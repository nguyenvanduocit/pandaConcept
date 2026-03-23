import os
from pathlib import Path

import requests

from .base import BaseProvider, RenderResult


class StabilityProvider(BaseProvider):
    """Stability AI (Stable Diffusion 3) image generation provider."""

    API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    def __init__(self) -> None:
        api_key = os.environ.get("STABILITY_API_KEY")
        if not api_key:
            raise ValueError("STABILITY_API_KEY environment variable is required")
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Stability AI"

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

        data = {
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": self._resolve_aspect_ratio(width, height),
        }
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        else:
            data["negative_prompt"] = (
                "cartoon, drawing, sketch, low quality, blurry, distorted, watermark, text"
            )

        try:
            response = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Accept": "image/*",
                },
                files={"none": ""},
                data=data,
                timeout=120,
            )
            response.raise_for_status()

            output_dir = Path("output/stability")
            output_dir.mkdir(parents=True, exist_ok=True)

            import time

            image_path = output_dir / f"sd3_{int(time.time())}.png"
            image_path.write_bytes(response.content)

            results.append(
                RenderResult(
                    provider=self.name,
                    image_path=image_path,
                    image_url=None,
                    prompt_used=prompt,
                    parameters={"model": "sd3", "aspect_ratio": data["aspect_ratio"]},
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
                    parameters={"model": "sd3"},
                    success=False,
                    error=str(e),
                )
            )

        return results

    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        return (
            f"photorealistic interior design, {base_prompt}, {style} style, "
            f"professional photography, 8k uhd, ray tracing, detailed textures, "
            f"natural lighting, architectural visualization"
        )

    @staticmethod
    def _resolve_aspect_ratio(width: int, height: int) -> str:
        """Map dimensions to Stability AI supported aspect ratios."""
        ratio = width / height
        if ratio > 1.5:
            return "16:9"
        elif ratio > 1.2:
            return "3:2"
        elif ratio < 0.67:
            return "9:16"
        elif ratio < 0.83:
            return "2:3"
        else:
            return "1:1"
