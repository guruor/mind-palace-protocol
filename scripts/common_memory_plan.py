#!/usr/bin/env python3
"""Create read-only common-memory write plans and test safe resume behavior."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

import yaml

from common_memory_payload import build_payload, run_scenario as run_payload_scenario


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "protocol/release-index.yaml"
BUDGET = ROOT / "protocol/provider-budgets.yaml"


class RateLimited(Exception):
    def __init__(self, retry_after: float) -> None:
        super().__init__(f"rate limited; retry after {retry_after} seconds")
        self.retry_after = retry_after


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected an object: {path}")
    return value


def _finish_plan(plan: dict[str, Any], budget: dict[str, Any]) -> dict[str, Any]:
    limits = budget["operation"]
    summary = plan["summary"]
    checks = (
        ("records", "max_records"),
        ("text_bytes", "max_text_bytes"),
        ("attachments", "max_attachments"),
        ("requests", "max_requests"),
    )
    for actual, maximum in checks:
        if summary[actual] > limits[maximum]:
            plan["reasons"].append(f"{actual} exceeds {maximum}")
    plan["allowed"] = not plan["reasons"]
    size = limits["batch_size"]
    ids = [item["id"] for item in plan["writes"] if item["action"] != "retain"]
    plan["batches"] = [ids[start : start + size] for start in range(0, len(ids), size)]
    return plan


def stage_plan(index: dict[str, Any], budget: dict[str, Any], source_revision: str) -> dict[str, Any]:
    core = [item for item in index["resources"] if item["class"] == "core"]
    _, proof = build_payload(source_revision)
    text_bytes = proof["payload_bytes"]
    version = index["protocol"]["version"]
    plan = {
        "operation": "stage",
        "provider": budget["provider"],
        "allowed": False,
        "reasons": [],
        "summary": {
            "records": 1,
            "text_bytes": text_bytes,
            "attachments": 0,
            "requests": 2,
            "rollback_writes": 1,
        },
        "writes": [
            {
                "id": f"mind-palace-release-{version}",
                "action": "create",
                "bytes": text_bytes,
                "core_resources": [item["path"] for item in core],
                "payload_digest": proof["payload_digest"],
                "release_index_digest": proof["release_index_digest"],
            }
        ],
        "batches": [],
        "rollback": ["Mark the staged release blocked; keep the active pointer unchanged."],
    }
    return _finish_plan(plan, budget)


def cache_plan(
    resource: dict[str, Any],
    budget: dict[str, Any],
    cached_paths: set[str],
    cached_bytes: int,
) -> dict[str, Any]:
    reasons = []
    if resource["class"] not in {"core", "on-demand"} or resource["cache"] == "never":
        reasons.append("resource is not cache eligible")
    if resource["path"] in cached_paths:
        action = "retain"
    else:
        action = "create"
        if len(cached_paths) >= budget["cache"]["max_records"]:
            reasons.append("cache record budget is full")
        if resource["bytes"] > budget["cache"]["max_resource_bytes"]:
            reasons.append("resource exceeds cache item budget")
        if cached_bytes + resource["bytes"] > budget["cache"]["max_bytes"]:
            reasons.append("resource exceeds total cache byte budget")
    records = 0 if action == "retain" else 1
    plan = {
        "operation": "cache",
        "provider": budget["provider"],
        "allowed": False,
        "reasons": reasons,
        "summary": {
            "records": records,
            "text_bytes": 0 if action == "retain" else resource["bytes"],
            "attachments": 0,
            "requests": records,
            "rollback_writes": records,
        },
        "writes": [{"id": resource["path"], "action": action, "bytes": resource["bytes"]}],
        "batches": [],
        "rollback": ["Remove only the new cache entry."] if records else [],
    }
    return _finish_plan(plan, budget)


def execute_plan(
    plan: dict[str, Any],
    writer: Callable[[dict[str, Any]], None],
    completed: set[str] | None = None,
) -> dict[str, Any]:
    if not plan["allowed"]:
        raise ValueError("refusing an over-budget or ineligible write plan")
    done = set(completed or set())
    for batch in plan["batches"]:
        for write_id in batch:
            if write_id in done:
                continue
            item = next(item for item in plan["writes"] if item["id"] == write_id)
            try:
                writer(item)
            except RateLimited as exc:
                return {"status": "rate-limited", "completed": sorted(done), "retry_after": exc.retry_after}
            done.add(write_id)
    return {"status": "complete", "completed": sorted(done)}


def run_scenario() -> None:
    run_payload_scenario()
    index = load_yaml(INDEX)
    budget = load_yaml(BUDGET)
    stage = stage_plan(index, budget, "synthetic-revision")
    if not stage["allowed"] or stage["summary"]["records"] != 1:
        raise ValueError("compact staging plan is not within budget")
    write = stage["writes"][0]
    if not write["payload_digest"].startswith("sha256:") or not write["release_index_digest"].startswith("sha256:"):
        raise ValueError("compact staging plan lacks payload proof")

    denied_budget = json.loads(json.dumps(budget))
    denied_budget["operation"]["max_text_bytes"] = 1
    denied = stage_plan(index, denied_budget, "synthetic-revision")
    calls: list[str] = []
    try:
        execute_plan(denied, lambda item: calls.append(item["id"]))
    except ValueError:
        pass
    else:
        raise ValueError("over-budget plan was executed")
    if calls:
        raise ValueError("over-budget plan called the writer")

    resource = next(item for item in index["resources"] if item["class"] == "on-demand")
    cache = cache_plan(resource, budget, set(), 0)
    if not cache["allowed"]:
        raise ValueError("eligible resource was not admitted to cache")
    reused = cache_plan(resource, budget, {resource["path"]}, resource["bytes"])
    if not reused["allowed"] or reused["writes"][0]["action"] != "retain":
        raise ValueError("existing cache resource was not reused")
    maintenance = next(item for item in index["resources"] if item["class"] == "maintenance")
    if cache_plan(maintenance, budget, set(), 0)["allowed"]:
        raise ValueError("maintenance resource was admitted to cache")

    writes = [
        {"id": f"write-{number}", "action": "create", "bytes": 1}
        for number in range(3)
    ]
    resume_plan = {
        "operation": "repair",
        "provider": "synthetic",
        "allowed": True,
        "reasons": [],
        "summary": {"records": 3, "text_bytes": 3, "attachments": 0, "requests": 3, "rollback_writes": 3},
        "writes": writes,
        "batches": [["write-0", "write-1"], ["write-2"]],
        "rollback": ["Remove synthetic writes."],
    }
    attempted: list[str] = []

    def limited_writer(item: dict[str, Any]) -> None:
        attempted.append(item["id"])
        if item["id"] == "write-1":
            raise RateLimited(30)

    stopped = execute_plan(resume_plan, limited_writer)
    if stopped != {"status": "rate-limited", "completed": ["write-0"], "retry_after": 30}:
        raise ValueError("rate-limited progress was not preserved")
    resumed: list[str] = []
    result = execute_plan(resume_plan, lambda item: resumed.append(item["id"]), set(stopped["completed"]))
    if result["status"] != "complete" or resumed != ["write-1", "write-2"]:
        raise ValueError("resume repeated or skipped writes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation", choices=("stage", "cache"), default="stage")
    parser.add_argument("--resource", help="release-index path for a cache plan")
    parser.add_argument("--source-revision", help="immutable source revision for a stage plan")
    args = parser.parse_args()
    try:
        index = load_yaml(INDEX)
        budget = load_yaml(BUDGET)
        if args.operation == "stage":
            if not args.source_revision:
                raise ValueError("--source-revision is required for a stage plan")
            plan = stage_plan(index, budget, args.source_revision)
        else:
            if not args.resource:
                raise ValueError("--resource is required for a cache plan")
            resource = next((item for item in index["resources"] if item["path"] == args.resource), None)
            if resource is None:
                raise ValueError(f"resource is not in the release index: {args.resource}")
            plan = cache_plan(resource, budget, set(), 0)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"write planning failed: {exc}")
        return 1
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0 if plan["allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
