#!/usr/bin/env python3
"""Create read-only common-memory write plans and test safe resume behavior."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import yaml

from build_awareness_core import OUTPUT as AWARENESS_CORE
from build_awareness_core import digest_of
from build_awareness_core import expected_text as render_awareness_core


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


def source_pointer(index: dict[str, Any], source_revision: str) -> dict[str, Any]:
    verified_resources = []
    for item in index["resources"]:
        if item["class"] != "core":
            continue
        content = (ROOT / item["path"]).read_bytes()
        digest = f"sha256:{hashlib.sha256(content).hexdigest()}"
        if len(content) != item["bytes"] or digest != item["digest"]:
            raise ValueError(f"core resource differs from Release Index: {item['path']}")
        verified_resources.append({"path": item["path"], "bytes": item["bytes"], "digest": item["digest"]})
    index_bytes = INDEX.read_bytes()
    awareness_text = render_awareness_core()
    awareness_bytes = len(awareness_text.encode("utf-8"))
    raw_root = f"https://raw.githubusercontent.com/guruor/mind-palace-protocol/{source_revision}"
    return {
        "pointer": {
            "source_revision": source_revision,
            "release_index": {
                "path": "protocol/release-index.yaml",
                "digest": f"sha256:{hashlib.sha256(index_bytes).hexdigest()}",
                "locator": f"{raw_root}/protocol/release-index.yaml",
            },
        },
        "verified_core_resources": verified_resources,
        "awareness": {
            "path": "protocol/awareness-core.md",
            "digest": digest_of(awareness_text),
            "bytes": awareness_bytes,
        },
    }


def _finish_plan(plan: dict[str, Any], budget: dict[str, Any]) -> dict[str, Any]:
    limits = budget["operation"]
    summary = plan["summary"]
    checks = (
        ("records", "max_records"),
        ("text_bytes", "max_text_bytes"),
        ("attachments", "max_attachments"),
        ("attachment_bytes", "max_attachment_bytes"),
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
    proof = source_pointer(index, source_revision)
    version = index["protocol"]["version"]
    if not AWARENESS_CORE.is_file() or AWARENESS_CORE.read_text(encoding="utf-8") != render_awareness_core():
        raise ValueError("protocol/awareness-core.md is stale")
    plan = {
        "operation": "stage",
        "provider": budget["provider"],
        "allowed": False,
        "reasons": [],
        "summary": {
            "records": 1,
            "text_bytes": proof["awareness"]["bytes"],
            "attachments": 0,
            "attachment_bytes": 0,
            "requests": 2,
            "rollback_writes": 1,
        },
        "writes": [
            {
                "id": f"mind-palace-release-{version}",
                "action": "create",
                "bytes": 0,
                "transport": "source-pointer-plus-awareness-core",
                "package_locator": f"https://github.com/guruor/mind-palace-protocol/tree/{source_revision}",
                "source_pointer": proof["pointer"],
                "awareness": proof["awareness"],
                "verification": {"core_resources": proof["verified_core_resources"]},
            }
        ],
        "batches": [],
        "rollback": ["Mark the staged release blocked; keep the active pointer unchanged."],
    }
    return _finish_plan(plan, budget)


def cleanup_plan(record_ids: list[str], budget: dict[str, Any]) -> dict[str, Any]:
    batch_size = budget["operation"]["batch_size"]
    selected = record_ids[:batch_size]
    records = len(selected)
    plan = {
        "operation": "cleanup",
        "provider": budget["provider"],
        "allowed": False,
        "reasons": [],
        "summary": {
            "records": records,
            "text_bytes": 0,
            "attachments": 0,
            "attachment_bytes": 0,
            "requests": records,
            "rollback_writes": records,
        },
        "writes": [{"id": record_id, "action": "remove", "bytes": 0} for record_id in selected],
        "batches": [],
        "remaining": record_ids[batch_size:],
        "rollback": ["Recreate a removed release pointer from its immutable repository release."],
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
    index = load_yaml(INDEX)
    budget = load_yaml(BUDGET)
    stage = stage_plan(index, budget, "synthetic-revision")
    if not stage["allowed"] or stage["summary"]["records"] != 1:
        raise ValueError("compact staging plan is not within budget")
    pointer = stage["writes"][0]["source_pointer"]
    proof = stage["writes"][0]["verification"]
    awareness = stage["writes"][0]["awareness"]
    if pointer["source_revision"] != "synthetic-revision" or len(proof["core_resources"]) != 5:
        raise ValueError("compact staging plan lacks an exact source pointer")
    if awareness["path"] != "protocol/awareness-core.md" or not awareness["digest"].startswith("sha256:"):
        raise ValueError("compact staging plan lacks an exact awareness core")
    if stage["summary"]["text_bytes"] <= 0:
        raise ValueError("compact staging plan does not account for awareness content bytes")

    denied_budget = json.loads(json.dumps(budget))
    denied_budget["operation"]["max_records"] = 0
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

    cleanup = cleanup_plan(["old-1", "old-2", "old-3"], budget)
    if not cleanup["allowed"] or cleanup["batches"] != [["old-1", "old-2"]]:
        raise ValueError("cleanup plan is not provider bounded")
    if cleanup["remaining"] != ["old-3"]:
        raise ValueError("cleanup plan did not preserve resumable work")

    writes = [
        {"id": f"write-{number}", "action": "create", "bytes": 1}
        for number in range(3)
    ]
    resume_plan = {
        "operation": "repair",
        "provider": "synthetic",
        "allowed": True,
        "reasons": [],
        "summary": {"records": 3, "text_bytes": 3, "attachments": 0, "attachment_bytes": 0, "requests": 3, "rollback_writes": 3},
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
    parser.add_argument("--operation", choices=("stage", "cleanup"), default="stage")
    parser.add_argument("--record", action="append", default=[], help="obsolete record ID for cleanup")
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
            if not args.record:
                raise ValueError("at least one --record is required for a cleanup plan")
            plan = cleanup_plan(args.record, budget)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"write planning failed: {exc}")
        return 1
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0 if plan["allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
