#!/usr/bin/env python3
"""Verify a document migration plan's immutable scope and execution gates."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCOPE_FIELDS = ("request", "target", "documents", "budget", "rollback", "validation")


def load_plan(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("migration plan must be an object")
    return value


def scope_digest(plan: dict[str, Any]) -> str:
    scope = {field: plan[field] for field in SCOPE_FIELDS}
    canonical = json.dumps(scope, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def execution_errors(plan: dict[str, Any]) -> list[str]:
    errors = []
    approval = plan["approval"]
    if approval["scope_digest"] != scope_digest(plan):
        errors.append("scope digest does not match the reviewed plan")
    if plan["state"] != "approved" or approval["status"] != "approved":
        errors.append("migration plan is not approved for execution")
    if not plan["budget"]["allowed"]:
        errors.append("migration plan exceeds its provider budget")
    for gate, checks in plan["checks"].items():
        blocked = [check["id"] for check in checks if check["status"] in {"failed", "unknown"}]
        if blocked:
            errors.append(f"{gate} gate is unresolved: {sorted(blocked)}")
    return errors


def run_scenario() -> None:
    plan = load_plan(ROOT / "tests/fixtures/valid/migration-plan.json")
    if plan["approval"]["scope_digest"] != scope_digest(plan):
        raise ValueError("migration fixture scope digest is stale")
    if not execution_errors(plan):
        raise ValueError("pending migration plan was accepted for execution")

    approved = json.loads(json.dumps(plan))
    approved["state"] = "approved"
    approved["approval"].update(
        {"status": "approved", "approved_by": "synthetic-user", "approved_at": "2026-01-01T00:00:00Z"}
    )
    if execution_errors(approved):
        raise ValueError("approved migration plan was rejected")

    changed = json.loads(json.dumps(approved))
    changed["documents"][0]["action"] = "skip"
    if not any("scope digest" in error for error in execution_errors(changed)):
        raise ValueError("changed migration scope retained approval")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--check-executable", action="store_true")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        digest = scope_digest(plan)
        errors = execution_errors(plan) if args.check_executable else None
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"migration plan failed: {exc}")
        return 1
    result: dict[str, Any] = {"scope_digest": digest}
    if errors is not None:
        result.update({"executable": not errors, "errors": errors})
    print(json.dumps(result, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
