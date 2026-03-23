# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pandaConcept is a Python project that provides AI-powered interior design workflows. It generates optimized image prompts, renders designs via multiple AI providers, and offers design consultation — covering 42 interior design styles worldwide.

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

42 styles across 5 categories:
- **Modern & Contemporary** (6): Minimalist, Scandinavian, Mid-Century Modern, Japandi, Contemporary, Bauhaus
- **Classic & Traditional** (10): Baroque, Colonial, Victorian, Neoclassical, Art Deco, French Provincial, Regency, Georgian, Rococo, Tudor
- **Asian & Eastern** (10): Japanese, Chinese, Vietnamese, Indochine, Korean, Thai, Balinese, Moroccan, Indian, Persian
- **Regional & Vernacular** (8): Mediterranean (Greek, Italian, Spanish), Tropical, Coastal, Rustic, Farmhouse, Desert/Southwestern
- **Specialty & Avant-Garde** (8): Industrial, Brutalist, Biophilic, Maximalist, Retro/Vintage, Futuristic, Bohemian, Wabi-Kintsugi

## Project Structure

```
pandaConcept/
├── src/                    # Source code
│   ├── providers/          # AI provider adapters
│   ├── styles/             # Design style definitions
│   ├── prompts/            # Prompt templates and builders
│   ├── consultation/       # Design consultation logic
│   └── utils/              # Shared utilities
├── projects/               # Design projects (one folder per project)
│   ├── .template/          # Template for new projects (copy this)
│   └── <project-name>/     # Each project contains:
│       ├── brief.md        #   Client requirements & project overview
│       ├── rooms.md        #   Room list with per-room requirements
│       ├── style-config.yaml #  Style, colors, materials, provider settings
│       ├── notes.md        #   Feedback, revision history, internal notes
│       ├── prompts/        #   Generated prompts for this project
│       ├── references/     #   Client reference images
│       │   ├── preprocessed/  # Depth maps, edge maps, segmentation (from /preprocess-room)
│       │   └── masks/         # Binary masks for inpainting (from /mask-room)
│       └── renders/        #   Output renders from providers
├── tests/                  # Test suite
├── .claude/skills/         # Claude Code skills for design workflows
└── pyproject.toml          # Project manifest
```

## Working with Projects

- To start a new project: copy `projects/.template/` to `projects/<project-name>/`
- Fill in `brief.md` first (client info, requirements, constraints)
- Define rooms in `rooms.md`, configure style in `style-config.yaml`
- Use `/design-consult` with the brief to get style recommendations
- Generated prompts and renders are saved within the project folder

## Design Workflow Skills

12 skills available via slash commands. They connect into 6 main flows:

### Flow 0: Design Interview (Recommended start — vague requirements)

```
/design-interview → /design-consult → /mood-board → /generate-prompt → /render → /compare-models
```

1. **`/design-interview`** — Phỏng vấn Socratic với ambiguity scoring — hỏi từng câu, chấm điểm clarity trên 6 chiều (Space, Style, Material/Color, Function, Mood/Lighting, Provider) — chỉ chuyển sang workflow khi ambiguity ≤ 20%. Tự động điền `brief.md`, `rooms.md`, `style-config.yaml` cho project.

### Flow 1: New Design (from scratch)

```
/design-consult → /mood-board → /generate-prompt → /render → /compare-models
```

1. **`/design-consult`** — Thu thập yêu cầu (room, style, mood, budget) → gợi ý 2-3 style → xuất design brief (color palette, materials, furniture, lighting)
2. **`/mood-board`** — Từ style + room → tạo mood board chi tiết (color story, textures, furniture, lighting, sensory experience)
3. **`/generate-prompt`** — Từ style + room + details → sinh prompt tối ưu cho từng provider (Gemini, OpenAI, Stability, Midjourney, Grok, Flux)
4. **`/render`** — Gửi prompt đến API providers → lưu ảnh vào `output/[style]/[provider]/`
5. **`/compare-models`** — So sánh output nhiều providers (style accuracy, photorealism, composition, detail, color fidelity)

### Flow 2: Redesign from Reference Photo (layout-preserving)

```
Ảnh phòng gốc → /preprocess-room → /generate-prompt → /render (with control maps) → /validate-layout → /compare-models
```

1. **`/preprocess-room`** — Extract depth map + canny edge + MLSD + segmentation từ ảnh phòng gốc → lưu vào `references/preprocessed/`. Bước BẮT BUỘC khi muốn giữ layout.
2. **`/generate-prompt`** — Sinh prompt theo style mới
3. **`/render`** — Gửi prompt + control maps đến Stability AI `/control/structure` hoặc Flux depth-pro → ảnh mới giữ đúng hình khối phòng gốc
4. **`/validate-layout`** — So sánh depth map trước/sau bằng SSIM → chấm điểm layout preservation (>= 0.70 = PASS)

### Flow 3: Targeted Element Editing (surgical changes)

```
Ảnh phòng → /mask-room → /edit-design → /render (inpainting) → /validate-layout
```

1. **`/mask-room`** — SAM2-based masking: chọn vùng cần thay đổi (chỉ sofa, chỉ tường, chỉ sàn) → tạo binary mask
2. **`/edit-design`** — Phân tích ảnh gốc + tạo edit prompt cho vùng mask
3. **`/render`** — Gửi ảnh + mask + prompt đến inpainting API → chỉ vùng mask thay đổi, phần còn lại giữ nguyên pixel-perfect

### Flow 4: Full Edit Design (from reference image, no layout control)

```
User gửi ảnh + yêu cầu thay đổi → /edit-design → /render
```

1. **`/edit-design`** — Phân tích ảnh gốc (scene inventory: objects, surfaces, materials, colors, lighting, camera) → tạo change diff (KEEP/MODIFY/ADD/REMOVE) → sinh prompt mới giữ nguyên phần không đổi, chỉ sửa phần cần thay → hỗ trợ cả full re-render và inpainting prompt

### Flow 5: Iterative Refinement

```
Ảnh chưa đạt → /refine → /render → lặp lại
```

1. **`/refine`** — Nhận prompt cũ + feedback → phân tích vấn đề (style, color, composition, detail, realism) → sinh prompt mới với tracked diff → gợi ý đổi provider nếu cần

### Reference & Utility Skills

- **`/style-guide`** — Tra cứu 42 design styles (keywords, materials, colors, characteristics). Được dùng bởi các skill khác khi cần vocabulary chính xác cho từng style.
- **`/validate-layout`** — So sánh depth map gốc vs ảnh mới, chấm điểm SSIM. Dùng sau `/render` khi cần đảm bảo layout.

### Skill Connection Map

```
                    /style-guide (reference cho tất cả)
                         │
                  /design-interview ← (start here khi yêu cầu mơ hồ)
                         │
                         │ (fills brief.md, rooms.md, style-config.yaml)
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
/design-consult    /edit-design          /refine
    │                    │                    │
/mood-board         /mask-room               │
    │                    │                    │
/generate-prompt    /preprocess-room          │
    │                    │                    │
    └────────┬───────────┘                    │
             │                                │
          /render ←───────────────────────────┘
             │
      /validate-layout
             │
      /compare-models
```

## Project Context Rules (CRITICAL)

**Before ANY design work**, you MUST:

1. **Ask which project** — Hỏi user đang làm project nào, hoặc tự detect từ context
2. **Read project files** — Đọc các file sau theo thứ tự:
   - `projects/<name>/brief.md` — để hiểu yêu cầu khách hàng
   - `projects/<name>/rooms.md` — để biết phòng nào cần làm, yêu cầu gì
   - `projects/<name>/style-config.yaml` — để dùng đúng style, color, materials
   - `projects/<name>/notes.md` — để biết feedback trước đó, tránh lặp lỗi cũ
3. **Check existing renders** — Xem `projects/<name>/renders/` và `projects/<name>/prompts/` để biết đã làm gì rồi
4. **Cross-check output** — Sau khi generate prompt hoặc render, kiểm tra lại với `style-config.yaml` và `brief.md` xem có khớp không

**Khi nào phải kiểm tra:**
- `/design-interview` → đọc project files hiện có (nếu có) để pre-fill, output ghi vào `brief.md` + `rooms.md` + `style-config.yaml`
- `/design-consult` → đọc `brief.md` trước, output ghi vào `brief.md` hoặc `notes.md`
- `/generate-prompt` → đọc `style-config.yaml` + `rooms.md`, output lưu vào `prompts/`
- `/preprocess-room` → đọc ảnh từ `references/`, output lưu vào `references/preprocessed/`
- `/render` → đọc prompt từ `prompts/` + control maps từ `references/preprocessed/` (nếu có), output lưu vào `renders/`
- `/mask-room` → đọc ảnh từ `references/` hoặc `renders/`, output lưu vào `references/masks/`
- `/validate-layout` → đọc depth map từ `references/preprocessed/` + ảnh từ `renders/`, ghi kết quả vào `notes.md`
- `/refine` → đọc `notes.md` (feedback cũ) + prompt cũ từ `prompts/`
- `/edit-design` → đọc `brief.md` + ảnh gốc từ `references/`
- `/compare-models` → đọc renders từ `renders/`, ghi kết quả vào `notes.md`

**KHÔNG BAO GIỜ:**
- Generate prompt mà không đọc `style-config.yaml` trước
- Render mà không biết đang làm project nào
- Bỏ qua feedback trong `notes.md` khi refine
- Quên cập nhật `rooms.md` (render status) sau khi render xong

## Conventions

- Use type hints throughout
- Provider adapters must implement the base provider interface
- Style definitions are data-driven (YAML/JSON), not hardcoded
- Keep prompt templates separate from generation logic
