#!/usr/bin/env python3
"""Validate a client installation receipt against this protocol release."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MIGRATION_CHECKS = (
    "package_integrity",
    "protocol_resolution",
    "methodology_resolution",
    "binding_resolution",
    "trust_isolation",
    "read_probe",
    "proposal_probe",
    "conflict_probe",
    "handoff_probe",
)
ALLOWED_RESOLUTIONS = {
    "absent": {"not-needed"},
    "same": {"not-needed"},
    "older-compatible": {"not-needed", "approved-upgrade"},
    "older-migration-required": {
        "approved-upgrade",
        "parallel-install",
        "retained-read-only",
        "blocked",
    },
    "newer": {
        "approved-downgrade",
        "parallel-install",
        "retained-read-only",
        "blocked",
    },
    "unversioned": {
        "approved-upgrade",
        "parallel-install",
        "retained-read-only",
        "blocked",
    },
    "invalid": {"retained-read-only", "blocked"},
}
APPROVAL_RESOLUTIONS = {"approved-upgrade", "approved-downgrade", "parallel-install"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("installation receipt must be an object")
    return value


def load_manifest() -> dict[str, Any]:
    with (ROOT / "protocol/manifest.yaml").open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError("protocol manifest must be an object")
    return value


def version_tuple(version: str) -> tuple[int, int, int]:
    core = version.split("+", 1)[0].split("-", 1)[0]
    major, minor, patch = core.split(".")
    return int(major), int(minor), int(patch)


def installation_errors(receipt: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    schema = load_json(ROOT / "schemas/client-installation.schema.json")
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(receipt)]
    if errors:
        return errors

    protocol = receipt["protocol"]
    if protocol["id"] != manifest["id"] or protocol["version"] != manifest["version"]:
        errors.append("receipt protocol release does not match the installed package")

    bindings = {item["id"] for item in manifest["bindings"]}
    if receipt["binding"] not in bindings:
        errors.append("selected binding is not present in the installed package")

    methodologies = {item["id"]: item["version"] for item in manifest["methodologies"]}
    for selected in receipt["methodologies"]:
        if methodologies.get(selected["id"]) != selected["version"]:
            errors.append(f"selected methodology release is unavailable: {selected['id']}")

    previous = receipt["previous_installation"]
    state = previous["state"]
    resolution = previous["resolution"]
    if resolution not in ALLOWED_RESOLUTIONS[state]:
        errors.append(f"resolution {resolution!r} is invalid for prior state {state!r}")
    if resolution in APPROVAL_RESOLUTIONS and not previous.get("approval_reference"):
        errors.append("approved prior-version resolution requires approval_reference")
    if resolution == "parallel-install" and previous.get("prior_write_authority") not in {
        "disabled",
        "read-only",
        "separate-instance",
    }:
        errors.append("parallel installation must isolate prior write authority")

    previous_version = previous.get("version")
    previous_source_version = previous.get("source_version")
    current_version = manifest["version"]
    if state == "same" and previous_version != current_version:
        errors.append("same prior state must report the installed protocol version")
    if state == "same" and previous_source_version != receipt["package"]["source_version"]:
        errors.append("same version must have the same immutable package identity")
    if state.startswith("older-"):
        if not previous_version or version_tuple(previous_version) >= version_tuple(current_version):
            errors.append("older prior state must report an older protocol version")
    if state == "newer":
        if not previous_version or version_tuple(previous_version) <= version_tuple(current_version):
            errors.append("newer prior state must report a newer protocol version")
    if state in {"older-compatible", "older-migration-required", "newer"} and not previous_source_version:
        errors.append("versioned prior installation must report immutable package identity")

    if receipt["migration_ready"]:
        if receipt["access_mode"] != "update":
            errors.append("migration readiness requires update access")
        for check in REQUIRED_MIGRATION_CHECKS:
            if receipt["checks"][check] != "pass":
                errors.append(f"migration readiness requires passing check: {check}")
        if state == "invalid" or resolution in {"blocked", "retained-read-only"}:
            errors.append("unresolved prior installation prevents migration readiness")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        errors = installation_errors(load_json(args.receipt), load_manifest())
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"installation validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"installation validation failed: {error}", file=sys.stderr)
        return 1
    print("Mind Palace client installation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
