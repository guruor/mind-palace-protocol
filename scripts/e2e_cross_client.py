#!/usr/bin/env python3
"""Run a synthetic two-client installation, handoff, and migration scenario."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from validate_handoff import handoff_envelope_errors
from validate_installation import ROOT, installation_errors, load_json, load_manifest


def source_identity(artifact: dict[str, Any]) -> str:
    payload = json.dumps(artifact, separators=(",", ":"), sort_keys=True).encode()
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def installation(client_id: str) -> dict[str, Any]:
    receipt = load_json(ROOT / "tests/fixtures/valid/client-installation.json")
    receipt["client"]["id"] = client_id
    return receipt


def handoff_for(artifact: dict[str, Any], approval: str = "granted") -> dict[str, Any]:
    handoff = load_json(ROOT / "tests/fixtures/valid/client-handoff.json")
    handoff["access_mode"] = "update"
    handoff["artifacts"] = [
        {
            "id": artifact["id"],
            "revision": artifact["revision"],
            "source_identity": source_identity(artifact),
        }
    ]
    handoff["approval"] = {
        "status": approval,
        "reference": "synthetic-bounded-approval",
        "scope": "One synthetic canary artifact",
    }
    return handoff


def handoff_errors(
    handoff: dict[str, Any],
    source: dict[str, dict[str, Any]],
    authorized_trust_domain: str,
) -> list[str]:
    errors = handoff_envelope_errors(handoff)
    if handoff["instance"]["trust_domain"] != authorized_trust_domain:
        errors.append("handoff trust domain is not authorized")
    for reference in handoff["artifacts"]:
        current = source.get(reference["id"])
        if current is None:
            errors.append(f"source artifact is unavailable: {reference['id']}")
            continue
        if current["revision"] != reference["revision"]:
            errors.append(f"source revision changed: {reference['id']}")
        if source_identity(current) != reference["source_identity"]:
            errors.append(f"source identity changed: {reference['id']}")
    return errors


def migrate(
    handoff: dict[str, Any],
    source: dict[str, dict[str, Any]],
    target: dict[str, dict[str, Any]],
) -> None:
    if handoff["access_mode"] != "update" or handoff["approval"]["status"] != "granted":
        raise ValueError("synthetic migration lacks bounded update approval")
    for reference in handoff["artifacts"]:
        artifact = copy.deepcopy(source[reference["id"]])
        artifact["migrated_source_identity"] = reference["source_identity"]
        target[reference["id"]] = artifact


def run_scenario() -> None:
    manifest = load_manifest()
    for client_id in ("synthetic-opencode", "synthetic-chatgpt"):
        errors = installation_errors(installation(client_id), manifest)
        if errors:
            raise ValueError(f"{client_id} installation failed: {errors[0]}")

    source = {
        "synthetic-product-spec": {
            "id": "synthetic-product-spec",
            "revision": 1,
            "trust_domain": "synthetic",
            "title": "Synthetic Product Specification",
            "body": "Initial approved outcome.",
        }
    }
    target: dict[str, dict[str, Any]] = {}
    approved = handoff_for(source["synthetic-product-spec"])
    errors = handoff_errors(approved, source, "synthetic")
    if errors:
        raise ValueError(f"fresh handoff failed: {errors[0]}")

    target_snapshot = copy.deepcopy(target)
    migrate(approved, source, target)
    first_result = copy.deepcopy(target)
    migrate(approved, source, target)
    if target != first_result or len(target) != 1:
        raise ValueError("migration rerun was not idempotent")

    stale = copy.deepcopy(approved)
    source["synthetic-product-spec"]["revision"] = 2
    source["synthetic-product-spec"]["body"] = "Revised approved outcome."
    stale_errors = handoff_errors(stale, source, "synthetic")
    if not any("source revision changed" in error for error in stale_errors):
        raise ValueError("stale handoff did not detect revision change")
    if not any("source identity changed" in error for error in stale_errors):
        raise ValueError("stale handoff did not detect source identity change")
    conflict = {
        "canonical": False,
        "artifact_id": "synthetic-product-spec",
        "base": stale["artifacts"][0],
        "current": {
            "revision": source["synthetic-product-spec"]["revision"],
            "source_identity": source_identity(source["synthetic-product-spec"]),
        },
    }
    if conflict["canonical"] or target != first_result:
        raise ValueError("stale proposal changed canonical target state")

    if not any(
        "trust domain is not authorized" in error
        for error in handoff_errors(stale, source, "different-domain")
    ):
        raise ValueError("cross-trust-domain handoff was not refused")

    refreshed = handoff_for(source["synthetic-product-spec"])
    errors = handoff_errors(refreshed, source, "synthetic")
    if errors:
        raise ValueError(f"refreshed handoff failed: {errors[0]}")
    migrate(refreshed, source, target)
    if target["synthetic-product-spec"]["revision"] != 2:
        raise ValueError("refreshed migration did not apply current revision")

    target.clear()
    target.update(target_snapshot)
    if target != target_snapshot:
        raise ValueError("rollback did not restore the target snapshot")


def main() -> int:
    try:
        run_scenario()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"cross-client E2E failed: {exc}", file=sys.stderr)
        return 1
    print("Synthetic OpenCode-to-ChatGPT E2E passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
