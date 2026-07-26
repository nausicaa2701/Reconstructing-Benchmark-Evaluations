#!/usr/bin/env python3
"""Verify model access without making generation requests."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from common import load_config, load_dotenv


def get(url: str, headers: dict[str, str]) -> dict:
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:500]
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def main() -> None:
    load_dotenv()
    config = load_config()["models"]
    checks = {
        "openai": (
            "OPENAI_API_KEY",
            f"https://api.openai.com/v1/models/{config['openai']['model']}",
            lambda key: {"Authorization": f"Bearer {key}"},
        ),
        "anthropic": (
            "ANTHROPIC_API_KEY",
            f"https://api.anthropic.com/v1/models/{config['anthropic']['model']}",
            lambda key: {"x-api-key": key, "anthropic-version": "2023-06-01"},
        ),
        "gemini": (
            "GEMINI_API_KEY",
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + urllib.parse.quote(config["gemini"]["model"], safe=""),
            lambda key: {"x-goog-api-key": key},
        ),
    }
    failed = False
    for provider, (variable, url, headers) in checks.items():
        key = os.environ.get(variable, "")
        if not key:
            print(f"{provider}: MISSING {variable}")
            failed = True
            continue
        try:
            response = get(url, headers(key))
            model = response.get("id") or response.get("name") or response.get("display_name")
            print(f"{provider}: OK ({model})")
        except Exception as exc:
            print(f"{provider}: ERROR ({exc})")
            failed = True
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()

