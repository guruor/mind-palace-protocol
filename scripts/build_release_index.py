#!/usr/bin/env python3
"""Build or verify the compact protocol release index."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import yaml

from validate_installation import load_manifest


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "protocol/resources.yaml"
OUTPUT = ROOT / "protocol/release-index.yaml"


def render() -> str:
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    resources = []
    seen: set[str] = set()
    for item in catalog["resources"]:
        path = item["path"]
        if path in seen:
            raise ValueError(f"duplicate release resource: {path}")
        seen.add(path)
        source = ROOT / path
        if not source.is_file():
            raise ValueError(f"release resource is not a file: {path}")
        payload = source.read_bytes()
        resources.append(
            {
                "path": path,
                "digest": f"sha256:{hashlib.sha256(payload).hexdigest()}",
                "bytes": len(payload),
                "class": item["class"],
                "cache": item["cache"],
                "purpose": item["purpose"],
            }
        )
    index = {
        "protocol": {"id": "mind-palace", "version": load_manifest()["version"]},
        "source": catalog["source"],
        "resources": resources,
    }
    return yaml.safe_dump(index, sort_keys=False, allow_unicode=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when the generated index is stale")
    args = parser.parse_args()
    try:
        expected = render()
        if args.check:
            if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
                raise ValueError("protocol/release-index.yaml is stale")
        else:
            OUTPUT.write_text(expected, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"release index failed: {exc}")
        return 1
    print("Release index is current." if args.check else "Release index generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
