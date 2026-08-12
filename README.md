# Open WebUI Misc

A collection of miscellaneous [Open WebUI](https://github.com/open-webui/open-webui) skills for generating high-quality image-to-video prompts.

This repository contains ready-to-use skill files that can be imported directly into Open WebUI to extend your assistant with specialized video-prompt-generation capabilities.

## 📦 Skills Included

| Skill | Description |
|-------|-------------|
| [`candid-video-prompts`](Skills/candid-video-prompts.md) | Generate three diverse 100–200 word image-to-video motion prompts from a reference image, styled as casual candid cellphone footage. |
| [`dynamic-action-video-prompts`](Skills/dynamic-action-video-prompts.md) | Transform a static reference image into three diverse short action-scene prompts for image-to-video generation, while preserving the original subjects, environment, and visual identity. |

## ✨ Features

- **Candid cellphone aesthetic** — both skills produce prompts that feel like spontaneous, handheld recordings rather than polished cinematic productions.
- **Three-prompt diversity** — each skill generates three meaningfully different prompts, not simple rephrasings of the same action.
- **Reference-image grounding** — prompts animate what is already in the image, preserving subjects, environment, composition, and visual identity without inventing unsupported elements.
- **Physically plausible motion** — realistic weight, momentum, acceleration, and secondary motion, avoiding teleportation, rubbery limbs, and impossible camera movement.
- **Structured quality checks** — both skills include built-in silent quality checklists to verify output before responding.

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

## 🗂️ Repository Structure

```
.
├── Skills/
│   ├── candid-video-prompts.md          # Candid motion prompt generator
│   └── dynamic-action-video-prompts.md  # Dynamic action scene prompt generator
├── .github/                             # GitHub community health files
├── .gitignore
├── LICENSE
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- [Open WebUI](https://github.com/open-webui/open-webui) — the platform these skills are designed for.