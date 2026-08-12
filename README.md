# Open WebUI Misc

A collection of miscellaneous [Open WebUI](https://github.com/open-webui/open-webui) skills for generating high-quality image-to-video prompts.

This repository contains ready-to-use skill files that can be imported directly into Open WebUI to extend your assistant with specialized video-prompt-generation capabilities.

## 📦 Skills Included

| Skill | Description |
|-------|-------------|
| [`candid-video-prompts`](Skills/candid-video-prompts.md) | Generate three diverse 100–200 word image-to-video motion prompts from a reference image, styled as casual candid cellphone footage. |
| [`dynamic-action-video-prompts`](Skills/dynamic-action-video-prompts.md) | Transform a static reference image into three diverse short action-scene prompts for image-to-video generation, while preserving the original subjects, environment, and visual identity. |
| [`candid-video-prompts-MiniMaxH3`](Skills/candid-video-prompts-MiniMaxH3.md) | MiniMax H3 variant of the candid skill — generates three diverse 100–200 word image-to-video motion prompts, each paired with a matching audio description (overall soundscape) for multimodal generation. |
| [`dynamic-action-video-prompts-MiniMaxH3`](Skills/dynamic-action-video-prompts-MiniMaxH3.md) | MiniMax H3 variant of the dynamic-action skill — transforms a static reference image into three distinct short action-scene prompts, each with a synchronized soundscape prompt for audio-visual generation. |

## ✨ Features

- **Candid cellphone aesthetic** — all skills produce prompts that feel like spontaneous, handheld recordings rather than polished cinematic productions.
- **Three-prompt diversity** — each skill generates three meaningfully different prompts, not simple rephrasings of the same action.
- **Reference-image grounding** — prompts animate what is already in the image, preserving subjects, environment, composition, and visual identity without inventing unsupported elements.
- **Physically plausible motion** — realistic weight, momentum, acceleration, and secondary motion, avoiding teleportation, rubbery limbs, and impossible camera movement.
- **Structured quality checks** — all skills include built-in silent quality checklists to verify output before responding.
- **Multimodal audio support (MiniMax H3)** — the MiniMax H3 variants pair every visual prompt with a synchronized audio description (overall soundscape), matching the scene, movement, and candid cellphone-recording aesthetic for audio-visual generation models.

## 🚀 Getting Started

### Prerequisites

- [Open WebUI](https://github.com/open-webui/open-webui) (installed and running)
- Access to an image-to-video generation model

### Installation

1. Open Open WebUI.
2. Navigate to the **Skills** / **Models** management area.
3. Create a new skill and paste the contents of the desired skill file:
   - [`Skills/candid-video-prompts.md`](Skills/candid-video-prompts.md)
   - [`Skills/dynamic-action-video-prompts.md`](Skills/dynamic-action-video-prompts.md)
   - [`Skills/candid-video-prompts-MiniMaxH3.md`](Skills/candid-video-prompts-MiniMaxH3.md)
   - [`Skills/dynamic-action-video-prompts-MiniMaxH3.md`](Skills/dynamic-action-video-prompts-MiniMaxH3.md)
4. Save the skill and attach it to your model or chat as needed.

Alternatively, clone this repository and copy the skill files into your Open WebUI skills directory:

```bash
git clone https://github.com/lunar-me/open-webui-misc.git
```

## 📖 Usage

1. Provide an image-to-video request along with a reference image to the model.
2. The skill generates exactly **3 prompts**, each **100–200 words**.
3. Pick a prompt and feed it to your image-to-video generation model.

Each prompt focuses on **motion and temporal change** — subject movement, expressions, gestures, environmental activity, lighting changes, and natural camera behavior — rather than redesigning the scene.

## 🛠️ Useful Scripts

### `image_chat.py`

A Python script that sends an image (plus optional text and configured Open WebUI tools/skills) to a local Open WebUI instance and saves the model's reply as a Markdown file.

**Workflow** (per [`docs/api-endpoints.md`](docs/api-endpoints.md)):

`image_chat.py` embeds the image inline as base64 directly in the chat message (standard OpenAI vision `image_url` format) — there is no upload, no server-side file processing (OCR/embeddings), and no polling:

1. Encode the image as an inline base64 `image_url`
2. Chat with the image + tools/skills → `POST /api/chat/completions`
3. Save the reply as a `.md` file

This is **near-instant** and guarantees the model receives the actual image — not the file's text representation (which appears as garbled binary on some cloud vision models).

**Prerequisites:**

- Python 3.10+ with the `requests` library (`pip install requests`)
- A running local Open WebUI instance
- An API key (from **Settings > Account** in Open WebUI)

**Usage:**

```bash
# Chat with an image + tool + skill
python image_chat.py path/to/image.png \
    --tool-id server:mcp:YOUR_MCP_SERVER_ID \
    --skill-id YOUR_SKILL_ID \
    --text "Describe this image" \
    --model qwen3.6:27b \
    --api-key YOUR_API_KEY \
    --output result.md

# List all available tools (IDs, names, descriptions)
python image_chat.py --list-tools --api-key YOUR_API_KEY

# List all available skills (IDs, names, descriptions)
python image_chat.py --list-skills --api-key YOUR_API_KEY
```

**Configuration via `.env`:** Copy [`.env.example`](.env.example) to `.env` and fill in your values. The script automatically loads `OPEN_WEBUI_API_KEY`, `OPEN_WEBUI_BASE_URL`, `OPEN_WEBUI_MODEL`, `OPEN_WEBUI_TOOL_ID`, `OPEN_WEBUI_SKILL_ID`, and `OPEN_WEBUI_LOG`. CLI flags override `.env` values.

## 🗂️ Repository Structure

```
.
├── Skills/
│   ├── candid-video-prompts.md                    # Candid motion prompt generator
│   ├── dynamic-action-video-prompts.md            # Dynamic action scene prompt generator
│   ├── candid-video-prompts-MiniMaxH3.md          # Candid motion + audio prompt generator (MiniMax H3)
│   └── dynamic-action-video-prompts-MiniMaxH3.md  # Dynamic action + sound prompt generator (MiniMax H3)
├── docs/
│   └── api-endpoints.md                          # Open WebUI API endpoint reference
├── .env.example                                  # Example environment configuration
├── .github/                             # GitHub community health files
├── .gitignore
├── image_chat.py                                 # Image + tool/skill chat script
├── LICENSE
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- [Open WebUI](https://github.com/open-webui/open-webui) — the platform these skills are designed for.