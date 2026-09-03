#!/usr/bin/env python3
"""Validate that a release tag matches the protocol manifest version."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_installation import load_manifest


TAG = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_release.py <tag>", file=sys.stderr)
        return 2
    tag = sys.argv[1]
    match = TAG.fullmatch(tag)
    if not match:
        print(f"release validation failed: invalid tag {tag!r}", file=sys.stderr)
        return 1
    expected = f"v{load_manifest()['version']}"
    if tag != expected:
        print(
            f"release validation failed: tag {tag!r} does not match {expected!r}",
            file=sys.stderr,
        )
        return 1
    notes = Path(__file__).resolve().parents[1] / "docs" / "releases" / f"{tag}.md"
    if not notes.is_file():
        print(
            f"release validation failed: missing release notes {notes}",
            file=sys.stderr,
        )
        return 1
    print(f"Release tag {tag} matches the protocol manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
