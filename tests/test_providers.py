from src.providers.base import BaseProvider, RenderResult
from src.providers.registry import PROVIDERS, list_providers


def test_list_providers():
    providers = list_providers()
    assert "openai" in providers
    assert "gemini" in providers
    assert "grok" in providers
    assert "stability" in providers
    assert "flux" in providers


def test_all_providers_implement_base():
    for name, cls in PROVIDERS.items():
        assert issubclass(cls, BaseProvider), f"{name} must subclass BaseProvider"


def test_render_result_creation():
    result = RenderResult(
        provider="test",
        image_path=None,
        image_url="https://example.com/image.png",
        prompt_used="test prompt",
        parameters={"model": "test"},
        success=True,
    )
    assert result.success
    assert result.error is None


def test_render_result_failure():
    result = RenderResult(
        provider="test",
        image_path=None,
        image_url=None,
        prompt_used="test prompt",
        parameters={},
        success=False,
        error="API key missing",
    )
    assert not result.success
    assert "API key" in result.error
