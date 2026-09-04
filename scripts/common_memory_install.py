#!/usr/bin/env python3
"""Exercise the idempotent common-memory installation state machine."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def release_resources(release: dict[str, Any]) -> list[dict[str, Any]]:
    """Return legacy, compact, or pointer-based runtime resources."""
    if "source_pointer" in release:
        return []
    return release.get("core_bundle", release.get("components", []))


def installation_errors(state: dict[str, Any]) -> list[str]:
    schema_path = ROOT / "schemas/common-memory-installation.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(state)]
    if errors:
        return errors
    release_ids = [item["id"] for item in state["releases"]]
    source_versions = [item["source_version"] for item in state["releases"]]
    if len(release_ids) != len(set(release_ids)):
        errors.append("release IDs must be unique")
    if len(source_versions) != len(set(source_versions)):
        errors.append("release source identities must be unique")
    active = [item for item in state["releases"] if item["status"] == "active"]
    if state["active_release"] is None and active:
        errors.append("inactive installation cannot contain an active release")
    if state["active_release"] is not None:
        if len(active) != 1 or active[0]["id"] != state["active_release"]:
            errors.append("active release pointer must identify the only active release")
    for release in state["releases"]:
        paths = [item["path"] for item in release_resources(release)]
        if len(paths) != len(set(paths)):
            errors.append(f"release contains duplicate runtime resource paths: {release['id']}")
    clients = [item["client_id"] for item in state["client_receipts"]]
    if len(clients) != len(set(clients)):
        errors.append("client receipt IDs must be unique")
    return errors


def version_tuple(version: str) -> tuple[int, int, int]:
    major, minor, patch = version.split("-", 1)[0].split("+", 1)[0].split(".")
    return int(major), int(minor), int(patch)


def install_release(
    state: dict[str, Any],
    candidate: dict[str, Any],
    approval_reference: str | None = None,
) -> tuple[str, dict[str, Any]]:
    result = copy.deepcopy(state)
    same_identity = next(
        (item for item in result["releases"] if item["source_version"] == candidate["source_version"]),
        None,
    )
    if same_identity:
        if same_identity["protocol"]["version"] != candidate["protocol"]["version"]:
            return "conflict", result
        if same_identity.get("release_index") != candidate.get("release_index"):
            return "conflict", result
        if same_identity.get("payload") != candidate.get("payload"):
            return "conflict", result
        if same_identity.get("source_pointer") != candidate.get("source_pointer"):
            return "conflict", result
        existing = {item["path"]: item for item in release_resources(same_identity)}
        for resource in release_resources(candidate):
            current = existing.get(resource["path"])
            if current and current["digest"] != resource["digest"]:
                return "conflict", result
        active = next(
            (item for item in result["releases"] if item["id"] == result["active_release"]),
            None,
        )
        if active and active["id"] != same_identity["id"]:
            candidate_version = version_tuple(candidate["protocol"]["version"])
            active_version = version_tuple(active["protocol"]["version"])
            if candidate_version < active_version:
                if not approval_reference:
                    return "blocked", result
                _activate(result, same_identity["id"])
                return "rolled-back", result
        missing = [item for item in release_resources(candidate) if item["path"] not in existing]
        if missing:
            target = "core_bundle" if "core_bundle" in same_identity else "components"
            same_identity[target].extend(copy.deepcopy(missing))
            return "repaired", result
        if same_identity["status"] == "staged" and approval_reference:
            _activate(result, same_identity["id"])
            return "upgraded", result
        return "no-op", result

    same_version = next(
        (
            item
            for item in result["releases"]
            if item["protocol"]["version"] == candidate["protocol"]["version"]
        ),
        None,
    )
    if same_version:
        return "conflict", result

    active = next(
        (item for item in result["releases"] if item["id"] == result["active_release"]),
        None,
    )
    new_release = copy.deepcopy(candidate)
    if active is None:
        new_release["status"] = "active"
        result["releases"].append(new_release)
        result["active_release"] = new_release["id"]
        return "installed", result
    if version_tuple(candidate["protocol"]["version"]) < version_tuple(active["protocol"]["version"]):
        return "blocked", result

    new_release["status"] = "staged"
    result["releases"].append(new_release)
    if approval_reference:
        _activate(result, new_release["id"])
        return "upgraded", result
    return "staged", result


def _activate(state: dict[str, Any], release_id: str) -> None:
    for release in state["releases"]:
        if release["id"] == release_id:
            release["status"] = "active"
        elif release["status"] == "active":
            release["status"] = "retired"
    state["active_release"] = release_id


def upsert_client_receipt(state: dict[str, Any], receipt: dict[str, str]) -> dict[str, Any]:
    result = copy.deepcopy(state)
    result["client_receipts"] = [
        item for item in result["client_receipts"] if item["client_id"] != receipt["client_id"]
    ]
    result["client_receipts"].append(copy.deepcopy(receipt))
    return result


def synthetic_release(version: str, source_version: str) -> dict[str, Any]:
    return {
        "id": f"mind-palace-{source_version}",
        "protocol": {"id": "mind-palace", "version": version},
        "package_locator": f"synthetic://mind-palace/{source_version}",
        "source_version": source_version,
        "status": "staged",
        "release_index": {
            "path": "protocol/release-index.yaml",
            "digest": "sha256:" + "0" * 64,
            "locator": f"synthetic://mind-palace/{source_version}/release-index",
        },
        "core_bundle": [
            {
                "path": "protocol/manifest.yaml",
                "digest": "sha256:" + "1" * 64,
                "locator": f"synthetic://mind-palace/{source_version}/manifest",
            },
            {
                "path": "protocol/general-guide.md",
                "digest": "sha256:" + "2" * 64,
                "locator": f"synthetic://mind-palace/{source_version}/guide",
            },
        ],
        "omissions": [],
    }


def synthetic_payload_release(version: str, source_version: str) -> dict[str, Any]:
    return {
        "id": f"mind-palace-{source_version}",
        "protocol": {"id": "mind-palace", "version": version},
        "package_locator": f"synthetic://mind-palace/{source_version}",
        "source_version": source_version,
        "status": "staged",
        "payload": {
            "filename": f"mind-palace-{version}-payload.md",
            "media_type": "text/markdown",
            "bytes": 100,
            "digest": "sha256:" + "3" * 64,
            "release_index_digest": "sha256:" + "4" * 64,
        },
        "omissions": [],
    }


def synthetic_pointer_release(version: str, source_version: str) -> dict[str, Any]:
    release = synthetic_release(version, source_version)
    release["source_pointer"] = {
        "source_revision": source_version,
        "release_index": release.pop("release_index"),
    }
    release.pop("core_bundle")
    return release


def cleanup_superseded_releases(state: dict[str, Any], active_release: str) -> tuple[list[str], dict[str, Any]]:
    """Remove protocol records only after the caller verifies client resolution."""
    if state.get("active_release") != active_release:
        raise ValueError("cleanup target is not the active release")
    result = copy.deepcopy(state)
    removed = [item["id"] for item in result["releases"] if item["id"] != active_release]
    result["releases"] = [item for item in result["releases"] if item["id"] == active_release]
    return removed, result


def empty_state() -> dict[str, Any]:
    return {
        "installation_id": "synthetic-mind-palace-installation",
        "trust_domain": "synthetic",
        "storage_binding": "notion",
        "active_release": None,
        "releases": [],
        "legacy_installations": [
            {
                "id": "legacy-guide",
                "locator": "synthetic://legacy-guide",
                "disposition": "retained-read-only",
            }
        ],
        "client_receipts": [],
    }


def run_scenario() -> None:
    original = empty_state()
    release = synthetic_release("0.1.0", "release-001")
    action, installed = install_release(original, release)
    if action != "installed" or original["releases"]:
        raise ValueError("first install was not isolated and successful")
    if installation_errors(installed):
        raise ValueError("first install produced invalid common-memory state")
    action, repeated = install_release(installed, release)
    if action != "no-op" or repeated != installed:
        raise ValueError("exact reinstall was not idempotent")

    damaged = copy.deepcopy(installed)
    damaged["releases"][0]["core_bundle"].pop()
    action, repaired = install_release(damaged, release)
    if action != "repaired" or repaired != installed:
        raise ValueError("missing core resource was not repaired")

    changed_index = copy.deepcopy(release)
    changed_index["release_index"]["digest"] = "sha256:" + "9" * 64
    action, unchanged = install_release(installed, changed_index)
    if action != "conflict" or unchanged != installed:
        raise ValueError("changed release index did not cause a conflict")

    repacked = synthetic_release("0.1.0", "different-release-001")
    action, unchanged = install_release(installed, repacked)
    if action != "conflict" or unchanged != installed:
        raise ValueError("same-version package conflict changed active state")

    payload_release = synthetic_payload_release("0.1.1", "payload-release-001")
    action, payload_staged = install_release(installed, payload_release)
    if action != "staged" or installation_errors(payload_staged):
        raise ValueError("attachment-backed release did not stage")
    changed_payload = copy.deepcopy(payload_release)
    changed_payload["payload"]["digest"] = "sha256:" + "5" * 64
    action, unchanged = install_release(payload_staged, changed_payload)
    if action != "conflict" or unchanged != payload_staged:
        raise ValueError("changed attachment payload did not cause a conflict")

    pointer_release = synthetic_pointer_release("0.1.2", "pointer-release-001")
    action, pointer_staged = install_release(installed, pointer_release)
    if action != "staged" or installation_errors(pointer_staged):
        raise ValueError("source-pointer release did not stage")
    changed_pointer = copy.deepcopy(pointer_release)
    changed_pointer["source_pointer"]["release_index"]["digest"] = "sha256:" + "6" * 64
    action, unchanged = install_release(pointer_staged, changed_pointer)
    if action != "conflict" or unchanged != pointer_staged:
        raise ValueError("changed source pointer did not cause a conflict")

    upgrade = synthetic_release("0.2.0", "release-002")
    action, staged = install_release(installed, upgrade)
    if action != "staged" or staged["active_release"] != installed["active_release"]:
        raise ValueError("upgrade did not stage beside active release")
    action, upgraded = install_release(staged, upgrade, "synthetic-approval")
    if action != "upgraded" or upgraded["active_release"] != upgrade["id"]:
        raise ValueError("approved upgrade did not activate")
    if installed["legacy_installations"] != upgraded["legacy_installations"]:
        raise ValueError("upgrade changed retained legacy installation")
    removed, cleaned = cleanup_superseded_releases(upgraded, upgrade["id"])
    if removed != [release["id"]] or [item["id"] for item in cleaned["releases"]] != [upgrade["id"]]:
        raise ValueError("post-resolution cleanup did not remove only superseded releases")
    if cleaned["legacy_installations"] != upgraded["legacy_installations"]:
        raise ValueError("post-resolution cleanup changed exempted legacy guidance")

    action, unchanged = install_release(upgraded, release)
    if action != "blocked" or unchanged != upgraded:
        raise ValueError("automatic downgrade was not blocked")
    action, rolled_back = install_release(upgraded, release, "synthetic-rollback-approval")
    if action != "rolled-back" or rolled_back["active_release"] != release["id"]:
        raise ValueError("approved rollback did not restore retained release")

    receipt = {"client_id": "synthetic-opencode", "receipt_locator": "synthetic://receipt/open"}
    with_receipt = upsert_client_receipt(upgraded, receipt)
    with_receipt = upsert_client_receipt(with_receipt, receipt)
    if len(with_receipt["client_receipts"]) != 1:
        raise ValueError("client receipt upsert created a duplicate")
    if installation_errors(with_receipt):
        raise ValueError("client receipt upsert produced invalid state")

    invalid_pointer = copy.deepcopy(upgraded)
    invalid_pointer["active_release"] = "missing-release"
    if not any("active release pointer" in error for error in installation_errors(invalid_pointer)):
        raise ValueError("invalid active release pointer was accepted")

    rollback = copy.deepcopy(upgraded)
    _activate(rollback, release["id"])
    if rollback["active_release"] != release["id"]:
        raise ValueError("rollback did not restore previous release")


def main() -> int:
    try:
        run_scenario()
    except ValueError as exc:
        print(f"common-memory installation failed: {exc}")
        return 1
    print("Common-memory installation scenario passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
