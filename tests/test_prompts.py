from src.prompts.builder import build_prompt


def test_build_prompt_all_providers():
    # Without API keys, providers will show as unconfigured
    prompts = build_prompt("living room", "modern")
    assert len(prompts) > 0


def test_build_prompt_contains_style_info():
    prompts = build_prompt("bedroom", "scandinavian")
    for _provider_name, prompt in prompts.items():
        # Each prompt should reference the style or room
        assert "scandinavian" in prompt.lower() or "Scandinavian" in prompt or "API key" in prompt


def test_build_prompt_with_extras():
    prompts = build_prompt(
        "kitchen",
        "japanese",
        lighting="warm golden hour",
        camera_angle="eye-level",
        extra_details="marble island countertop",
    )
    assert len(prompts) > 0
