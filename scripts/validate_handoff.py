#!/usr/bin/env python3
"""Validate a portable cross-client handoff envelope."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from validate_installation import ROOT, load_json, load_manifest


def handoff_envelope_errors(handoff: dict[str, Any]) -> list[str]:
    schema = load_json(ROOT / "schemas/client-handoff.schema.json")
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(handoff)]
    if errors:
        return errors

    manifest = load_manifest()
    protocol = handoff["protocol"]
    if protocol["id"] != manifest["id"] or protocol["version"] != manifest["version"]:
        errors.append("handoff protocol does not match the installed release")
    available = {item["id"]: item["version"] for item in manifest["methodologies"]}
    methodology = handoff["methodology"]
    if available.get(methodology["id"]) != methodology["version"]:
        errors.append("handoff methodology is unavailable")
    artifact_ids = [artifact["id"] for artifact in handoff["artifacts"]]
    if len(artifact_ids) != len(set(artifact_ids)):
        errors.append("handoff contains duplicate artifact IDs")
    approval = handoff["approval"]
    if approval["status"] in {"granted", "denied"} and not approval.get("reference"):
        errors.append("decided approval requires a reference")
    if approval["status"] == "granted" and not approval.get("scope"):
        errors.append("granted approval requires bounded scope")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    try:
        errors = handoff_envelope_errors(load_json(args.handoff))
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"handoff validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"handoff validation failed: {error}", file=sys.stderr)
        return 1
    print("Mind Palace cross-client handoff validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
