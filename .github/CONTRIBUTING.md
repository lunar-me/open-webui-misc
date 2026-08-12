# Contributing to Open WebUI Misc

Thank you for your interest in contributing! This project is a small, focused collection of Open WebUI skills, and we welcome improvements.

## How to Contribute

### 1. Open an Issue First (For Larger Changes)

For new skills, significant rewrites, or changes that affect behavior, please open an issue first to discuss the approach before writing code.

### 2. Fork and Branch

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 3. Make Your Changes

- Follow the existing style and structure of the skill files.
- Each skill file should have:
  - A YAML frontmatter block with `name` and `description`.
  - Clear, well-organized sections.
  - A silent quality-check section.
- Update the `README.md` table if you add a new skill.

### 4. Commit with a Clear Message

```bash
git commit -m "Add: new skill for XYZ"
```

Use conventional commit prefixes where helpful: `Add:`, `Fix:`, `Docs:`, `Refactor:`.

### 5. Open a Pull Request

- Provide a clear description of the change.
- Reference any related issue.
- Ensure your branch is up to date with `main` before opening the PR.

## Style Guide

- Use clear, imperative language in prompts.
- Keep prompts grounded in the reference image.
- Avoid cinematic clichés unless explicitly desired.
- Prefer concise, well-scoped sections over monolithic walls of text.

## Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).