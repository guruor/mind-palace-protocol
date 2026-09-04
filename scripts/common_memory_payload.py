#!/usr/bin/env python3
"""Build and verify the compact common-memory release payload."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "protocol/release-index.yaml"
LANGUAGES = {".json": "json", ".md": "markdown", ".yaml": "yaml", ".yml": "yaml"}


def digest(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def load_index() -> tuple[dict[str, Any], str]:
    text = INDEX.read_text(encoding="utf-8")
    value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("release index must be an object")
    return value, text


def core_paths(index: dict[str, Any]) -> list[str]:
    return [item["path"] for item in index["resources"] if item["class"] == "core"]


def build_payload(source_revision: str) -> tuple[str, dict[str, Any]]:
    index, index_text = load_index()
    resources = []
    indexed = {item["path"]: item for item in index["resources"]}
    for path in core_paths(index):
        content = (ROOT / path).read_text(encoding="utf-8")
        resource = {"path": path, "bytes": len(content.encode()), "digest": digest(content.encode())}
        if resource["bytes"] != indexed[path]["bytes"] or resource["digest"] != indexed[path]["digest"]:
            raise ValueError(f"core resource differs from Release Index: {path}")
        resources.append(resource)

    index_digest = digest(index_text.encode())
    lines = [
        "## Immutable package",
        f"- **Protocol:** `mind-palace` `{index['protocol']['version']}`",
        f"- **Source identity:** `{source_revision}`",
        f"- **Package:** [immutable GitHub commit](https://github.com/guruor/mind-palace-protocol/tree/{source_revision})",
        f"- **Release Index digest:** `{index_digest}`",
        "- **Projection:** one Release Index and six-resource Core Bundle",
        "- **Activation:** staged; the installation active pointer remains unchanged",
        "## Release Index",
        f"```yaml\n{index_text}```",
        "## Core Bundle",
    ]
    for resource in resources:
        content = (ROOT / resource["path"]).read_text(encoding="utf-8")
        language = LANGUAGES.get(Path(resource["path"]).suffix, "text")
        lines.extend((f"### `{resource['path']}`", f"```{language}\n{content}```"))
    lines.extend(
        (
            "## Payload proof",
            f"```json\n{json.dumps({'release_index': {'bytes': len(index_text.encode()), 'digest': index_digest}, 'resources': resources}, indent=2, sort_keys=True)}\n```",
            "## Safety boundary",
            "No private knowledge, credentials, client configuration, or executable extension code is included. This staged release does not change the installation active pointer, migrate documents, or clean up legacy records.",
        )
    )
    payload = "\n".join(lines)
    proof = {
        "payload_bytes": len(payload.encode()),
        "payload_digest": digest(payload.encode()),
        "release_index_digest": index_digest,
        "resources": resources,
    }
    return payload, proof


def _extract_fence(payload: str, heading: str) -> str:
    start = payload.find(f"{heading}\n```")
    if start < 0:
        raise ValueError(f"missing or reordered payload section: {heading}")
    body_start = payload.find("\n", start + len(heading) + 1) + 1
    body_end = payload.find("```", body_start)
    if body_start == 0 or body_end < 0:
        raise ValueError(f"unterminated payload section: {heading}")
    return payload[body_start:body_end]


def verify_payload(payload: str, source_revision: str) -> dict[str, Any]:
    expected, proof = build_payload(source_revision)
    headings = ["## Release Index"] + [f"### `{item['path']}`" for item in proof["resources"]]
    positions = [payload.find(heading) for heading in headings]
    if any(payload.count(heading) != 1 for heading in headings):
        raise ValueError("payload sections are missing or duplicated")
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise ValueError("payload sections are missing or reordered")
    expected_index = INDEX.read_text(encoding="utf-8")
    if _extract_fence(payload, "## Release Index") != expected_index:
        raise ValueError("embedded Release Index differs from source bytes")
    for resource in proof["resources"]:
        embedded = _extract_fence(payload, f"### `{resource['path']}`")
        if embedded != (ROOT / resource["path"]).read_text(encoding="utf-8"):
            raise ValueError(f"embedded resource differs from source bytes: {resource['path']}")
    if payload != expected:
        raise ValueError("payload wrapper or proof differs from deterministic output")
    return proof


def run_scenario() -> None:
    revision = "synthetic-revision"
    payload, proof = build_payload(revision)
    if build_payload(revision) != (payload, proof):
        raise ValueError("common-memory payload is not deterministic")
    verify_payload(payload, revision)
    mutations = (
        payload.replace("### `protocol/manifest.yaml`", "### `omitted`", 1),
        payload.replace("Define shared collaboration", "Define  shared collaboration", 1),
        payload.replace("### `protocol/manifest.yaml`", "### `protocol/manifest.yaml`\n### `protocol/manifest.yaml`", 1),
        payload.replace("### `protocol/manifest.yaml`", "### `__swap__`", 1)
        .replace("### `protocol/general-guide.md`", "### `protocol/manifest.yaml`", 1)
        .replace("### `__swap__`", "### `protocol/general-guide.md`", 1),
    )
    for mutation in mutations:
        try:
            verify_payload(mutation, revision)
        except ValueError:
            continue
        raise ValueError("invalid common-memory payload was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        proof = verify_payload(args.verify.read_text(encoding="utf-8"), args.source_revision)
    else:
        payload, proof = build_payload(args.source_revision)
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload)
    print(json.dumps(proof, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
