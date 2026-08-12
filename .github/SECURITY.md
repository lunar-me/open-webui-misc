# Security Policy

## Supported Versions

This project is a collection of Open WebUI skill prompt files. It is not a software application and does not process or store sensitive data. As such, there are no version-specific security patches.

| Version | Supported |
|---------|-----------|
| `main`  | ✅        |

## Reporting a Vulnerability

This project consists of prompt/instruction text files only. However, if you discover a vulnerability in the skills themselves (for example, prompt-injection risks, unsafe instructions, or unexpected behavior that could cause harm), please report it privately.

**Do not open a public issue for security vulnerabilities.**

Instead, report vulnerabilities by opening a [private security advisory](https://github.com/lunar-me/open-webui-misc/security/advisories/new) on GitHub.

You can expect an acknowledgement within **48 hours** and a status update within **7 days**.

## Security Considerations for Skill Files

Skills are instructions executed by a language model. Please keep the following in mind:

- Skill content should not instruct the model to bypass safety measures, exfiltrate data, or perform harmful actions.
- When reviewing pull requests, check that new skills do not introduce unsafe instructions.
- Prompts should remain grounded in user-provided reference images and not fabricate unsupported content.