from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RenderResult:
    """Result from an image generation API call."""

    provider: str
    image_path: Path | None
    image_url: str | None
    prompt_used: str
    parameters: dict
    success: bool
    error: str | None = None


class BaseProvider(ABC):
    """Base interface for all AI image generation providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider display name."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        negative_prompt: str | None = None,
        width: int = 1792,
        height: int = 1024,
        num_images: int = 1,
    ) -> list[RenderResult]:
        """Generate images from a prompt."""

    @abstractmethod
    def optimize_prompt(self, base_prompt: str, style: str) -> str:
        """Optimize a prompt for this specific provider."""
