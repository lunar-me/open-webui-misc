#!/usr/bin/env python3
"""
Sample script: send an image + optional text + configured Open WebUI tools
and/or skills to a local Open WebUI instance, and save the model's reply as
a Markdown file.

Workflow (per api-endpoints.md):
  1. Upload the image   -> POST /api/v1/files/
  2. Wait for processing -> GET /api/v1/files/{id}/process/status
  3. Chat with the file + tools/skills -> POST /api/chat/completions
  4. Save the reply as a .md file

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
import json
import os
import sys
import time
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://localhost:3000"
DEFAULT_MODEL = "qwen3.6:27b"
DEFAULT_POLL_INTERVAL = 2.0
DEFAULT_TIMEOUT = 300.0

ENV_FILE = ".env"
ENV_VARS = (
    "OPEN_WEBUI_API_KEY",
    "OPEN_WEBUI_BASE_URL",
    "OPEN_WEBUI_MODEL",
    "OPEN_WEBUI_TOOL_ID",
    "OPEN_WEBUI_SKILL_ID",
    "OPEN_WEBUI_POLL_INTERVAL",
    "OPEN_WEBUI_TIMEOUT",
)


class OpenWebUIClientError(Exception):
    """Base error for Open WebUI API failures."""


class FileUploadError(OpenWebUIClientError):
    """Raised when uploading a file fails."""


class FileProcessingError(OpenWebUIClientError):
    """Raised when file processing fails or times out."""


class ChatCompletionError(OpenWebUIClientError):
    """Raised when the chat completion request fails."""


class ToolsListError(OpenWebUIClientError):
    """Raised when listing tools fails."""


class SkillsListError(OpenWebUIClientError):
    """Raised when listing skills fails."""


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
        "--poll-interval",
        type=float,
        default=float(os.environ.get("OPEN_WEBUI_POLL_INTERVAL", DEFAULT_POLL_INTERVAL)),
        help=f"Poll interval seconds while waiting for file processing (default: {DEFAULT_POLL_INTERVAL}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("OPEN_WEBUI_TIMEOUT", DEFAULT_TIMEOUT)),
        help=f"Max seconds to wait for file processing (default: {DEFAULT_TIMEOUT}).",
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


def upload_file(base_url: str, headers: dict, image_path: Path) -> str:
    """Upload an image and return its file ID."""
    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    url = f"{base_url}/api/v1/files/"
    with open(image_path, "rb") as fh:
        files = {"file": (image_path.name, fh)}
        try:
            resp = requests.post(url, headers=headers, files=files, timeout=60)
        except requests.RequestException as exc:
            raise FileUploadError(f"Network error while uploading file: {exc}") from exc

    if resp.status_code != 200:
        raise FileUploadError(
            f"Upload failed with HTTP {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except json.JSONDecodeError as exc:
        raise FileUploadError(f"Upload returned invalid JSON: {resp.text}") from exc

    file_id = data.get("id")
    if not file_id:
        raise FileUploadError(f"Upload response missing 'id': {data}")
    return file_id


def wait_for_file_processing(
    base_url: str,
    headers: dict,
    file_id: str,
    poll_interval: float,
    timeout: float,
) -> None:
    """Poll the processing-status endpoint until the file is ready or fails."""
    url = f"{base_url}/api/v1/files/{file_id}/process/status"
    start = time.time()

    while time.time() - start < timeout:
        try:
            resp = requests.get(url, headers=headers, timeout=60)
        except requests.RequestException as exc:
            raise FileProcessingError(
                f"Network error while checking processing status: {exc}"
            ) from exc

        if resp.status_code != 200:
            raise FileProcessingError(
                f"Status check failed with HTTP {resp.status_code}: {resp.text}"
            )

        try:
            data = resp.json()
        except json.JSONDecodeError as exc:
            raise FileProcessingError(
                f"Status response invalid JSON: {resp.text}"
            ) from exc

        status = data.get("status")
        if status == "completed":
            return
        if status == "failed":
            raise FileProcessingError(
                f"File processing failed: {data.get('error', 'unknown error')}"
            )
        time.sleep(poll_interval)

    raise FileProcessingError(
        f"Timed out after {timeout}s waiting for file processing to complete."
    )


def chat_completion(
    base_url: str,
    headers: dict,
    model: str,
    file_id: str,
    text: str,
    tool_ids: list[str],
    skill_ids: list[str],
) -> str:
    """Call /api/chat/completions with the file + tools/skills and return the reply text."""
    url = f"{base_url}/api/chat/completions"
    content = text if text.strip() else "Describe this image."
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "files": [{"type": "file", "id": file_id}],
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

    # Extract the assistant reply text (OpenAI-compatible format).
    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise ChatCompletionError(f"Unexpected response shape: {data}") from exc


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

        print(f"[1/4] Uploading {args.image} ...")
        file_id = upload_file(args.base_url, headers, args.image)
        print(f"      -> file id: {file_id}")

        print("[2/4] Waiting for file processing ...")
        wait_for_file_processing(
            args.base_url, headers, file_id, args.poll_interval, args.timeout
        )
        print("      -> processing completed")

        print("[3/4] Requesting chat completion with tools/skills ...")
        reply = chat_completion(
            args.base_url,
            headers,
            args.model,
            file_id,
            args.text,
            args.tool_id,
            args.skill_id,
        )

        print(f"[4/4] Writing result to {output_path} ...")
        write_markdown(
            output_path,
            reply,
            args.image,
            args.text,
            args.tool_id,
            args.skill_id,
            args.model,
        )

        print(f"Done. Result saved to: {output_path}")
        return 0

    except (FileNotFoundError, ValueError, FileUploadError, FileProcessingError, ChatCompletionError) as exc:
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