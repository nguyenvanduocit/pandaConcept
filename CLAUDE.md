# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pandaConcept is a Python project that provides AI-powered interior design workflows. It generates optimized image prompts, renders designs via multiple AI providers, and offers design consultation — covering 30+ interior design styles worldwide.

## Tech Stack

- **Language**: Python 3.11+
- **AI Providers**: Google Gemini, OpenAI (DALL-E / GPT-4o), xAI Grok, Stability AI, Midjourney API, Flux
- **Package Manager**: pip with pyproject.toml

## Architecture

- Multi-provider design: each AI provider is a pluggable adapter behind a common interface
- Prompt templates are style-aware — each design style has specific keywords, characteristics, and rendering parameters per provider
- Provider-specific prompt optimization: different models need different prompt structures for best results

## Environment Variables

API keys are managed via environment variables (never hardcode):
- `GEMINI_API_KEY` — Google Gemini
- `OPENAI_API_KEY` — OpenAI (DALL-E, GPT-4o)
- `GROK_API_KEY` — xAI Grok
- `STABILITY_API_KEY` — Stability AI
- `MIDJOURNEY_API_KEY` — Midjourney
- `FLUX_API_KEY` — Flux

Use a `.env` file locally (gitignored). Reference `.env.example` for required keys.

## Prompt Engineering Conventions

- Prompts must specify: room type, design style, lighting, camera angle, materials, color palette
- Each provider has different optimal prompt lengths and keyword ordering
- Always include negative prompts where the provider supports them
- Style-specific vocabulary matters — use the style guide skill for reference

## Design Styles Coverage

Comprehensive coverage across categories:
- **Modern**: Modern, Minimalist, Scandinavian, Contemporary, Japandi, Mid-Century Modern
- **Classic**: Neoclassical, Victorian, Art Deco, French Provincial, Baroque, Colonial
- **Asian**: Japanese (Wabi-Sabi), Chinese, Vietnamese, Indochine, Korean, Thai
- **Regional**: Mediterranean, Tropical, Bohemian, Rustic, Farmhouse, Coastal
- **Specialty**: Industrial, Brutalist, Biophilic, Maximalist, Retro, Futuristic

## Project Structure

```
pandaConcept/
├── src/                    # Source code
│   ├── providers/          # AI provider adapters
│   ├── styles/             # Design style definitions
│   ├── prompts/            # Prompt templates and builders
│   ├── consultation/       # Design consultation logic
│   └── utils/              # Shared utilities
├── tests/                  # Test suite
├── .claude/skills/         # Claude Code skills for design workflows
└── pyproject.toml          # Project manifest
```

## Design Workflow Skills

8 skills available via slash commands. They connect into 3 main flows:

### Flow 1: New Design (from scratch)

```
/design-consult → /mood-board → /generate-prompt → /render → /compare-models
```

1. **`/design-consult`** — Thu thập yêu cầu (room, style, mood, budget) → gợi ý 2-3 style → xuất design brief (color palette, materials, furniture, lighting)
2. **`/mood-board`** — Từ style + room → tạo mood board chi tiết (color story, textures, furniture, lighting, sensory experience)
3. **`/generate-prompt`** — Từ style + room + details → sinh prompt tối ưu cho từng provider (Gemini, OpenAI, Stability, Midjourney, Grok, Flux)
4. **`/render`** — Gửi prompt đến API providers → lưu ảnh vào `output/[style]/[provider]/`
5. **`/compare-models`** — So sánh output nhiều providers (style accuracy, photorealism, composition, detail, color fidelity)

### Flow 2: Edit Design (from reference image)

```
User gửi ảnh + yêu cầu thay đổi → /edit-design → /render
```

1. **`/edit-design`** — Phân tích ảnh gốc (scene inventory: objects, surfaces, materials, colors, lighting, camera) → tạo change diff (KEEP/MODIFY/ADD/REMOVE) → sinh prompt mới giữ nguyên phần không đổi, chỉ sửa phần cần thay → hỗ trợ cả full re-render và inpainting prompt

### Flow 3: Iterative Refinement

```
Ảnh chưa đạt → /refine → /render → lặp lại
```

1. **`/refine`** — Nhận prompt cũ + feedback → phân tích vấn đề (style, color, composition, detail, realism) → sinh prompt mới với tracked diff → gợi ý đổi provider nếu cần

### Reference Skill

- **`/style-guide`** — Tra cứu 30+ design styles (keywords, materials, colors, characteristics). Được dùng bởi các skill khác khi cần vocabulary chính xác cho từng style.

### Skill Connection Map

```
                    /style-guide (reference cho tất cả)
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
/design-consult    /edit-design          /refine
    │                    │                    │
/mood-board              │                    │
    │                    │                    │
/generate-prompt         │                    │
    │                    │                    │
    └────────┬───────────┘                    │
             │                                │
          /render ←───────────────────────────┘
             │
      /compare-models
```

## Conventions

- Use type hints throughout
- Provider adapters must implement the base provider interface
- Style definitions are data-driven (YAML/JSON), not hardcoded
- Keep prompt templates separate from generation logic
