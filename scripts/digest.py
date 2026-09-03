#!/usr/bin/env python3
"""Calculate a stable SHA-256 digest for a portable Markdown artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


VOLATILE_KEYS = {"content_digest", "source_version", "updated_at"}


def without_volatile(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_volatile(item)
            for key, item in value.items()
            if key not in VOLATILE_KEYS
        }
    if isinstance(value, list):
        return [without_volatile(item) for item in value]
    return value


def split_artifact(text: str) -> tuple[dict[str, Any], str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        raise ValueError("artifact is missing YAML front matter")
    try:
        _, raw_metadata, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("artifact has unterminated YAML front matter") from exc
    metadata = yaml.safe_load(raw_metadata)
    if not isinstance(metadata, dict):
        raise ValueError("artifact front matter must be an object")
    return metadata, body.strip("\n") + "\n"


def canonical_digest(text: str) -> str:
    metadata, body = split_artifact(text)
    encoded_metadata = json.dumps(
        without_volatile(metadata),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    payload = f"{encoded_metadata}\n---\n{body}".encode()
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    print(canonical_digest(args.artifact.read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
