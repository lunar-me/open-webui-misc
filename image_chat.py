#!/usr/bin/env python3
"""
Sample script: send an image + optional text + configured Open WebUI tools
and/or skills to a local Open WebUI instance, and save the model's reply as
a Markdown file.

Workflow:
  1. Encode the image as an inline base64 data URI
  2. Chat with the image + tools/skills -> POST /api/chat/completions
  3. Save the reply as a .md file

The image is always embedded inline as base64 directly in the chat message
(standard OpenAI vision 'image_url' format). This is near-instant — there is
no upload, no server-side file processing (OCR/embeddings), and no polling —
and it guarantees the model receives the actual image rather than the file's
text representation (which appears as garbled binary on some cloud vision
models).

Usage:
  python image_chat.py path/to/image.png \
      --tool-id server:mcp:YOUR_MCP_SERVER_ID \
      --skill-id YOUR_SKILL_ID \
      --text "Describe this image" \
      --model qwen3.6:27b \
      --api-key YOUR_API_KEY \
      --output result.md

List all available tools (IDs, names, descriptions):
  python image_chat.py --list-tools \
      --api-key YOUR_API_KEY

List all available skills (IDs, names, descriptions):
  python image_chat.py --list-skills \
      --api-key YOUR_API_KEY
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://localhost:3000"
DEFAULT_MODEL = "qwen3.6:27b"

ENV_FILE = ".env"
ENV_VARS = (
    "OPEN_WEBUI_API_KEY",
    "OPEN_WEBUI_BASE_URL",
    "OPEN_WEBUI_MODEL",
    "OPEN_WEBUI_TOOL_ID",
    "OPEN_WEBUI_SKILL_ID",
    "OPEN_WEBUI_LOG",
)


class OpenWebUIClientError(Exception):
    """Base error for Open WebUI API failures."""


class ChatCompletionError(OpenWebUIClientError):
    """Raised when the chat completion request fails."""


class ToolsListError(OpenWebUIClientError):
    """Raised when listing tools fails."""


class SkillsListError(OpenWebUIClientError):
    """Raised when listing skills fails."""


class ModelNotFoundError(OpenWebUIClientError):
    """Raised when the requested model does not exist on the server."""


def load_env(env_file: Path | str = Path(ENV_FILE)) -> None:
    """
    Load KEY=VALUE lines from a .env file into os.environ.
    Existing environment variables take precedence; comments and
    blank lines are ignored. Values may be quoted with ' or ".
    """
    env_path = Path(env_file)
    if not env_path.is_file():
        return
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"WARNING: Could not read {env_file}: {exc}", file=sys.stderr)
        return

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] in "'\"" and value[-1] == value[0]:
            value = value[1:-1]
        # Only set if not already present in the environment.
        os.environ.setdefault(key, value)


def parse_args() -> argparse.Namespace:
    load_env()  # load .env values (lowest priority) before parsing args

    parser = argparse.ArgumentParser(
        description="Send an image + optional text + tools/skills to Open WebUI and save the reply as Markdown."
    )
    parser.add_argument(
        "image",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the image file to send (not needed with --list-tools or --list-skills).",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List all available tool IDs, names, and descriptions, then exit.",
    )
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="List all available skill IDs, names, and descriptions, then exit.",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="",
        help="Optional text/prompt to accompany the image.",
    )
    parser.add_argument(
        "--tool-id",
        action="append",
        default=(
            [os.environ["OPEN_WEBUI_TOOL_ID"]]
            if os.environ.get("OPEN_WEBUI_TOOL_ID")
            else []
        ),
        metavar="TOOL_ID",
        help="Open WebUI tool ID, e.g. 'server:mcp:YOUR_MCP_SERVER_ID'. Repeatable. Falls back to OPEN_WEBUI_TOOL_ID.",
    )
    parser.add_argument(
        "--skill-id",
        action="append",
        default=(
            [os.environ["OPEN_WEBUI_SKILL_ID"]]
            if os.environ.get("OPEN_WEBUI_SKILL_ID")
            else []
        ),
        metavar="SKILL_ID",
        help="Open WebUI skill ID to enable in the chat. Repeatable. Falls back to OPEN_WEBUI_SKILL_ID.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("OPEN_WEBUI_MODEL", DEFAULT_MODEL),
        help=f"Model ID to use (default: {DEFAULT_MODEL}, or OPEN_WEBUI_MODEL).",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=os.environ.get("OPEN_WEBUI_BASE_URL", DEFAULT_BASE_URL),
        help=f"Open WebUI base URL (default: {DEFAULT_BASE_URL}, or OPEN_WEBUI_BASE_URL).",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="API key (or JWT). Falls back to env var OPEN_WEBUI_API_KEY.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output .md file path (default: <image_stem>.md next to the image).",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        default=os.environ.get("OPEN_WEBUI_LOG", "").lower() in ("1", "true", "yes", "on"),
        help="Write an interaction log (input, thoughts, output) to <image_stem>.log. "
        "Enabled by default when OPEN_WEBUI_LOG is set to 1/true/yes/on.",
    )
    if len(sys.argv) < 2:
        # No arguments supplied: show help instead of an error.
        parser.print_help()
        raise SystemExit(0)
    return parser.parse_args()


def resolve_token(args: argparse.Namespace) -> str:
    """Resolve the API token from args or the OPEN_WEBUI_API_KEY env var."""
    token = args.api_key or os.environ.get("OPEN_WEBUI_API_KEY", "")
    if not token:
        raise ValueError(
            "No API key provided. Pass --api-key or set the OPEN_WEBUI_API_KEY environment variable."
        )
    return token


def build_headers(token: str) -> dict:
    """Construct authorization + content headers from a raw token."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _fetch_items(base_url: str, token: str, endpoint: str, kind: str) -> list:
    """
    Fetch a list of items (tools/skills) from an Open WebUI /api/v1 endpoint.

    Returns a list of item dicts. Raises OpenWebUIClientError on failure.
    """
    headers = build_headers(token)
    url = f"{base_url}{endpoint}"

    try:
        resp = requests.get(url, headers=headers, timeout=60)
    except requests.RequestException as exc:
        raise OpenWebUIClientError(f"Network error while listing {kind}s: {exc}") from exc

    if resp.status_code != 200:
        raise OpenWebUIClientError(
            f"List {kind}s failed with HTTP {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except json.JSONDecodeError as exc:
        raise OpenWebUIClientError(
            f"List {kind}s returned invalid JSON: {resp.text}"
        ) from exc

    # Open WebUI returns a list of dicts, each with an 'id'.
    if isinstance(data, dict):
        items = data.get("data", data.get(kind + "s", []))
    else:
        items = data if isinstance(data, list) else []

    return items


def _print_items(items: list, kind: str) -> None:
    """Print a list of items as: ID | Name | Description."""
    if not items:
        print(f"No {kind}s found.")
        return

    print(f"Found {len(items)} {kind}(s):\n")
    for item in items:
        item_id = item.get("id", item.get("name", "?"))
        name = item.get("name", item_id)
        # 'description' may be nested in 'meta' for function-based items.
        description = item.get("description") or ""
        if not description and isinstance(item.get("meta"), dict):
            description = item["meta"].get("description", "")
        print(f"ID          : {item_id}")
        print(f"Name        : {name}")
        print(f"Description : {description}")
        print("-" * 60)


def list_tools(base_url: str, token: str) -> None:
    """Fetch and print all available tools as: ID | Name | Description."""
    try:
        items = _fetch_items(base_url, token, "/api/v1/tools/", "tool")
    except OpenWebUIClientError as exc:
        raise ToolsListError(str(exc)) from exc
    _print_items(items, "tool")


def list_skills(base_url: str, token: str) -> None:
    """Fetch and print all available skills as: ID | Name | Description."""
    try:
        items = _fetch_items(base_url, token, "/api/v1/skills/", "skill")
    except OpenWebUIClientError as exc:
        raise SkillsListError(str(exc)) from exc
    _print_items(items, "skill")


def validate_model(base_url: str, headers: dict, model: str) -> None:
    """
    Fast check that the requested model exists on the server BEFORE any
    expensive work (file encoding) is done.

    Raises ModelNotFoundError if the model is not in GET /api/models.
    """
    url = f"{base_url}/api/models"
    try:
        resp = requests.get(url, headers=headers, timeout=60)
    except requests.RequestException as exc:
        raise OpenWebUIClientError(f"Network error while checking models: {exc}") from exc

    if resp.status_code != 200:
        raise OpenWebUIClientError(
            f"Model list failed with HTTP {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except json.JSONDecodeError as exc:
        raise OpenWebUIClientError(f"Model list returned invalid JSON: {resp.text}") from exc

    # Open WebUI returns {"data": [{"id": "...", ...}, ...]}.
    models = data.get("data", []) if isinstance(data, dict) else []
    model_ids: set[str] = set()
    for m in models:
        if isinstance(m, dict):
            mid = m.get("id")
            if isinstance(mid, str):
                model_ids.add(mid)

    if model not in model_ids:
        if model_ids:
            available = "\n  - " + "\n  - ".join(sorted(model_ids))
        else:
            available = "\n  (none)"
        raise ModelNotFoundError(
            f"Model '{model}' not found.\nAvailable models:{available}"
        )


def detect_mime_type(path: Path) -> str:
    """
    Determine the image MIME type from the file extension, falling back to
    magic-byte sniffing so base64 data URIs are always well-formed.
    """
    mime, _ = mimetypes.guess_type(path.name)
    if mime and mime.startswith("image/"):
        return mime

    head = path.read_bytes()[:16]
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head.startswith(b"GIF87a") or head.startswith(b"GIF89a"):
        return "image/gif"
    if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
        return "image/webp"

    return mime or "application/octet-stream"


def encode_image_data_uri(path: Path) -> str:
    """
    Read an image file and return a base64 data URI suitable for an OpenAI
    'image_url' content part, e.g. data:image/jpeg;base64,/9j/4AAQ...
    """
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")
    mime = detect_mime_type(path)
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_multimodal_content(text: str, image_data_uri: str) -> list:
    """
    Build the 'content' field for the user message as structured multimodal
    parts (OpenAI vision format): an inline image_url part, plus a text part
    only when a non-empty prompt is provided.
    """
    parts = [{"type": "image_url", "image_url": {"url": image_data_uri}}]
    if text and text.strip():
        parts.insert(0, {"type": "text", "text": text})
    return parts


def _extract_thoughts(message: dict) -> str:
    """
    Extract the model's reasoning/thinking text from an assistant message.

    Handles both flat fields ('reasoning', 'reasoning_content') and
    structured content blocks (type 'thinking' / 'reasoning' / 'analysis').
    Returns an empty string when no thoughts are present.
    """
    parts: list[str] = []

    for key in ("reasoning", "reasoning_content", "thinking"):
        val = message.get(key)
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())

    content = message.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if btype in ("thinking", "reasoning", "analysis"):
                btext = block.get("text") or block.get("content") or block.get("thinking")
                if isinstance(btext, str) and btext.strip():
                    parts.append(btext.strip())

    return "\n\n".join(parts)


def chat_completion(
    base_url: str,
    headers: dict,
    model: str,
    user_content: str | list,
    *,
    tool_ids: list[str] | None = None,
    skill_ids: list[str] | None = None,
) -> tuple[str, str]:
    """
    Call /api/chat/completions with the user message + tools/skills.

    `user_content` is passed through as structured multimodal content
    (text + inline base64 image_url).

    Returns a (reply_text, thoughts_text) tuple. thoughts_text is the model's
    reasoning/thinking (may be empty if the model does not expose it).
    """
    url = f"{base_url}/api/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_content}],
    }
    if tool_ids:
        payload["tool_ids"] = tool_ids
    if skill_ids:
        payload["skill_ids"] = skill_ids

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=300)
    except requests.RequestException as exc:
        raise ChatCompletionError(f"Network error during chat completion: {exc}") from exc

    if resp.status_code != 200:
        raise ChatCompletionError(
            f"Chat completion failed with HTTP {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except json.JSONDecodeError as exc:
        raise ChatCompletionError(f"Chat completion returned invalid JSON: {resp.text}") from exc

    # Extract the assistant reply text + thoughts (OpenAI-compatible format).
    try:
        message = data["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ChatCompletionError(f"Unexpected response shape: {data}") from exc

    reply = message.get("content") or ""
    if isinstance(reply, list):
        # Structured content blocks: join text blocks.
        reply = "\n".join(
            b.get("text", "")
            for b in reply
            if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str)
        ).strip()

    thoughts = _extract_thoughts(message)
    return reply, thoughts


def write_markdown(
    output_path: Path,
    reply: str,
    image_path: Path,
    text: str,
    tool_ids: list[str],
    skill_ids: list[str],
    model: str,
) -> None:
    """Save the reply (plus metadata) as a Markdown file."""
    front_matter = (
        "<!-- Generated by image_chat.py -->\n"
        f"<!-- image: {image_path} -->\n"
        f"<!-- model: {model} -->\n"
        f"<!-- tools: {', '.join(tool_ids) if tool_ids else '(none)'} -->\n"
        f"<!-- skills: {', '.join(skill_ids) if skill_ids else '(none)'} -->\n"
        f"<!-- prompt: {text or '(image only)'} -->\n\n"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(front_matter + reply + "\n", encoding="utf-8")


def log_interaction(
    log_path: Path,
    image_path: Path,
    text: str,
    model: str,
    tool_ids: list[str],
    skill_ids: list[str],
    attachment: str,
    thoughts: str,
    reply: str,
) -> None:
    """Write a human-readable interaction log: input, thoughts, and output."""
    lines = [
        "=" * 60,
        "Open WebUI interaction log",
        "=" * 60,
        "",
        "--- INPUT ---",
        f"image : {image_path}",
        f"attachment : {attachment}",
        f"model : {model}",
        f"tools : {', '.join(tool_ids) if tool_ids else '(none)'}",
        f"skills: {', '.join(skill_ids) if skill_ids else '(none)'}",
        f"prompt: {text or '(image only)'}",
        "",
        "--- THOUGHTS ---",
        thoughts if thoughts.strip() else "(no reasoning/thoughts returned)",
        "",
        "--- OUTPUT ---",
        reply,
        "",
        "=" * 60,
    ]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_list_tools(args: argparse.Namespace) -> int:
    """Handle the --list-tools mode."""
    try:
        token = resolve_token(args)
        list_tools(args.base_url, token)
        return 0
    except (ValueError, ToolsListError, requests.RequestException) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - catch-all last resort
        print(f"ERROR: Unexpected error: {exc!r}", file=sys.stderr)
        return 1


def run_list_skills(args: argparse.Namespace) -> int:
    """Handle the --list-skills mode."""
    try:
        token = resolve_token(args)
        list_skills(args.base_url, token)
        return 0
    except (ValueError, SkillsListError, requests.RequestException) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - catch-all last resort
        print(f"ERROR: Unexpected error: {exc!r}", file=sys.stderr)
        return 1


def run_chat(args: argparse.Namespace) -> int:
    """Handle the normal image + text + tools/skills chat flow."""
    output_path = args.output or (args.image.with_suffix(".md"))
    try:
        token = resolve_token(args)
        headers = build_headers(token)

        print(f"[0/3] Checking model '{args.model}' exists ...")
        validate_model(args.base_url, headers, args.model)
        print("      -> model found")

        print(f"[1/3] Encoding {args.image} as inline base64 image ...")
        image_data_uri = encode_image_data_uri(args.image)
        print(f"      -> {len(image_data_uri)}-char data URI "
              f"({detect_mime_type(args.image)})")

        print("[2/3] Requesting chat completion with tools/skills ...")
        user_content = build_multimodal_content(args.text, image_data_uri)
        reply, thoughts = chat_completion(
            args.base_url,
            headers,
            args.model,
            user_content,
            tool_ids=args.tool_id,
            skill_ids=args.skill_id,
        )

        print(f"[3/3] Writing result to {output_path} ...")
        write_markdown(
            output_path,
            reply,
            args.image,
            args.text,
            args.tool_id,
            args.skill_id,
            args.model,
        )

        if args.log:
            log_path = args.image.with_suffix(".log")
            print(f"      -> writing interaction log to {log_path}")
            log_interaction(
                log_path,
                args.image,
                args.text,
                args.model,
                args.tool_id,
                args.skill_id,
                "inline base64 image_url",
                thoughts,
                reply,
            )

        print(f"Done.")
        return 0

    except (FileNotFoundError, ValueError, ChatCompletionError, ModelNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"ERROR: Unexpected network failure: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - catch-all last resort
        print(f"ERROR: Unexpected error: {exc!r}", file=sys.stderr)
        return 1


def main() -> int:
    args = parse_args()

    if args.list_tools:
        return run_list_tools(args)

    if args.list_skills:
        return run_list_skills(args)

    if not args.image:
        print(
            "ERROR: An image path is required unless --list-tools or --list-skills is used.",
            file=sys.stderr,
        )
        return 2

    if not args.tool_id and not args.skill_id:
        print(
            "ERROR: At least one of --tool-id or --skill-id is required. "
            "Use --list-tools / --list-skills to see available options.",
            file=sys.stderr,
        )
        return 2

    return run_chat(args)


if __name__ == "__main__":
    sys.exit(main())
