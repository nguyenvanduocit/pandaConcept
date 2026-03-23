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

13 skills available via slash commands. They connect into 7 main flows:

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

### Flow 6: Video Generation (animate renders into cinematic videos)

```
Room renders → /generate-video (image-to-video) → /generate-video (extend) → /generate-video (merge tour) → /generate-video (upscale)
```

1. **`/generate-video`** — Tạo video từ renders hoặc text prompts sử dụng Veo (Gemini) và fal.ai. Hỗ trợ 6 mode: text-to-video, image-to-video, video extension (nối clip dài hơn), frame interpolation (before/after transition), room tour (merge nhiều clip), video upscaling. Output lưu vào `renders/videos/`.

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
             │
      /generate-video ← (animate renders thành video)
          │
          ├── image-to-video (từ render)
          ├── extend (nối clip dài hơn)
          ├── interpolate (before/after transition)
          ├── tour (merge nhiều phòng)
          └── upscale (tăng resolution video)
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
- `/generate-video` → đọc renders từ `renders/` (image-to-video) hoặc prompts từ `prompts/` (text-to-video), output lưu vào `renders/videos/`

**AUTO-TRIGGER Rules (CRITICAL — tự động làm, KHÔNG cần user nhắc):**

Khi user **đưa ảnh phòng** (reference photo, ảnh hiện trạng, ảnh phòng thật):
1. Xác định intent: **EDIT** (enhance, thêm detail, sáng hơn, realistic hơn) hay **REDESIGN** (đổi style hoàn toàn)?
2. Nếu **EDIT** → dùng Gemini image editing trực tiếp (image + text instruction), KHÔNG cần preprocess
3. Nếu **REDESIGN** → tự động chạy `/preprocess-room` → extract depth + canny + segmentation → lưu vào `references/preprocessed/` → dùng layout-controlled API
4. Sau khi render từ redesign, tự động chạy `/validate-layout` → báo SSIM score

Khi user **yêu cầu thay đổi một phần** ("đổi sofa", "sơn lại tường", "thay sàn"):
1. Tự động chạy `/mask-room` → tạo mask cho element cần đổi
2. Tự động dùng inpainting API thay vì full re-render
3. Phần ngoài mask giữ nguyên pixel-perfect

Khi user **yêu cầu edit/redesign từ ảnh** (bất kỳ ảnh nào):
1. Kiểm tra `references/preprocessed/` — nếu chưa có control maps → chạy `/preprocess-room` trước
2. `/edit-design` phải output cả full re-render prompt VÀ inpainting prompt
3. `/render` tự chọn: có mask → inpainting, có depth map → structure control, không có gì → text-only

Khi **render xong** (bất kỳ render nào từ reference photo):
1. Tự động chạy `/validate-layout` nếu có depth map gốc trong `references/preprocessed/`
2. Nếu SSIM < 0.70 → cảnh báo user và gợi ý tăng control_strength hoặc đổi provider
3. Ghi SSIM score vào `notes.md`

**Decision tree cho `/render`:**
```
Có ảnh gốc?
├── YES → User muốn gì?
│         ├── EDIT (enhance, add details, adjust tone, fix elements)
│         │   └── IMAGE EDITING MODE → Gemini (image + text instruction, không cần preprocess)
│         │
│         └── REDESIGN (đổi style, thiết kế lại hoàn toàn)
│             ├── Có preprocessed maps?
│             │   ├── YES → Có mask?
│             │   │         ├── YES → Inpainting API (Stability/OpenAI)
│             │   │         └── NO  → Structure control API (Stability/Gemini)
│             │   └── NO  → Chạy /preprocess-room trước → quay lại YES
│             └── (KHÔNG BAO GIỜ skip preprocess cho redesign)
└── NO  → Text-to-image bình thường (như cũ)
```

**EDIT vs REDESIGN:**
- **Edit** = enhance/tweak ảnh hiện có (thêm detail, sáng hơn, realistic hơn, đổi màu) → Gemini image editing trực tiếp, KHÔNG cần depth map
- **Redesign** = đổi style hoàn toàn, giữ layout → BẮT BUỘC có depth map + structure control

**KHÔNG BAO GIỜ:**
- Generate prompt mà không đọc `style-config.yaml` trước
- Render mà không biết đang làm project nào
- Bỏ qua feedback trong `notes.md` khi refine
- Quên cập nhật `rooms.md` (render status) sau khi render xong
- Render REDESIGN từ ảnh reference mà không preprocess trước (depth map là BẮT BUỘC cho redesign)
- Bỏ qua validate-layout khi đã có depth map gốc (chỉ áp dụng cho redesign, không cần cho edit)
- Dùng text-to-image khi đã có control maps (phải dùng structure control)
- Dùng sai Gemini model — CHỈ dùng `gemini-3.1-flash-image-preview`. Google trả error misleading ("API key expired", 404) khi model name sai
- Hỏi user API key khi key đã có trong `CLAUDE.local.md`

## Conventions

- Use type hints throughout
- Provider adapters must implement the base provider interface
- Style definitions are data-driven (YAML/JSON), not hardcoded
- Keep prompt templates separate from generation logic
