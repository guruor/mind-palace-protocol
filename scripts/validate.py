#!/usr/bin/env python3
"""Validate protocol schemas, fixtures, examples, links, and privacy invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from client_adapter_config import run_scenario as run_client_adapter_scenario
from common_memory_install import run_scenario as run_common_memory_install_scenario
from digest import canonical_digest
from e2e_cross_client import run_scenario
from validate_installation import installation_errors, load_manifest


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
PRIVATE_PATTERNS = (
    re.compile(r"https://(?:www\.)?notion\.so/", re.I),
    re.compile(r"https://app\.notion\.com/p/[0-9a-f]{32}", re.I),
    re.compile(r"(?:^|/)Users/[^/]+/", re.I),
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXCLUDED_DIRS = {".git", ".venv", "__pycache__"}


def maintained(path: Path) -> bool:
    return not EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas: dict[str, dict] = {}
    resources: list[tuple[str, Resource]] = []
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = load_json(path)
        if not isinstance(schema, dict) or not isinstance(schema.get("$id"), str):
            raise ValueError(f"schema lacks $id: {path.relative_to(ROOT)}")
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return schemas, Registry().with_resources(resources)


def validator(name: str, schemas: dict[str, dict], registry: Registry) -> Draft202012Validator:
    return Draft202012Validator(schemas[name], registry=registry)


def markdown_metadata(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML front matter: {path.relative_to(ROOT)}")
    try:
        _, raw, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"unterminated YAML front matter: {path.relative_to(ROOT)}") from exc
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise ValueError(f"front matter must be an object: {path.relative_to(ROOT)}")
    return value


def validate_fixtures(schemas: dict[str, dict], registry: Registry) -> None:
    artifact = validator("artifact.schema.json", schemas, registry)
    product = validator("product-engineering.schema.json", schemas, registry)
    installation = validator("client-installation.schema.json", schemas, registry)
    handoff = validator("client-handoff.schema.json", schemas, registry)

    for path in sorted((ROOT / "tests/fixtures/valid").glob("*.json")):
        selected = handoff if "client-handoff" in path.name else (
            installation if "client-installation" in path.name else (
                product if "product-engineering" in path.name else artifact
            )
        )
        errors = list(selected.iter_errors(load_json(path)))
        if errors:
            raise ValueError(f"valid fixture rejected: {path.relative_to(ROOT)}: {errors[0].message}")

    for path in sorted((ROOT / "tests/fixtures/invalid").glob("*.json")):
        selected = handoff if "client-handoff" in path.name else (
            installation if "client-installation" in path.name else (
                product if "product-engineering" in path.name else artifact
            )
        )
        if not list(selected.iter_errors(load_json(path))):
            raise ValueError(f"invalid fixture accepted: {path.relative_to(ROOT)}")

    for path in sorted((ROOT / "examples").glob("**/*.md")):
        metadata = markdown_metadata(path)
        selected = product if metadata.get("methodology", {}).get("id") == "product-engineering" else artifact
        errors = list(selected.iter_errors(metadata))
        if errors:
            raise ValueError(f"example rejected: {path.relative_to(ROOT)}: {errors[0].message}")

    templates = sorted((ROOT / "methodologies/product-engineering/templates").glob("*.md"))
    if len(templates) != 10:
        raise ValueError(f"expected 10 product-engineering templates, found {len(templates)}")
    for path in templates:
        errors = list(product.iter_errors(markdown_metadata(path)))
        if errors:
            raise ValueError(f"template rejected: {path.relative_to(ROOT)}: {errors[0].message}")

    conflict = ROOT / "protocol/conflict-template.md"
    errors = list(artifact.iter_errors(markdown_metadata(conflict)))
    if errors:
        raise ValueError(f"conflict template rejected: {conflict.relative_to(ROOT)}: {errors[0].message}")


def validate_markdown_links() -> None:
    for path in sorted(ROOT.glob("**/*.md")):
        if not maintained(path):
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "{{")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                raise ValueError(f"broken link in {path.relative_to(ROOT)}: {target}")


def validate_manifest() -> None:
    manifest = load_manifest()
    path_fields = (
        "general_guide",
        "installation_guide",
        "core_schema",
        "installation_schema",
        "handoff_schema",
        "client_adapter_contract",
        "conflict_template",
    )
    for field in path_fields:
        path = ROOT / manifest[field]
        if not path.is_file():
            raise ValueError(f"manifest path does not exist: {field}={manifest[field]}")
    for collection in ("methodologies", "bindings"):
        ids = [item["id"] for item in manifest[collection]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate IDs in manifest {collection}")
        for item in manifest[collection]:
            if not (ROOT / item["guide"]).is_file():
                raise ValueError(f"manifest guide does not exist: {item['guide']}")


def validate_privacy() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not maintained(path) or path.name == "uv.lock":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in PRIVATE_PATTERNS:
            if pattern.search(text):
                raise ValueError(f"private locator pattern in {path.relative_to(ROOT)}")


def validate_digest_invariants() -> None:
    first = """---
id: example
revision: 1
relations:
  - type: part_of
    target: project
updated_at: one
---

Body
"""
    reordered = """---\r
updated_at: two\r
relations: [{target: project, type: part_of}]\r
revision: 1\r
id: example\r
---\r
Body\r
\r
"""
    changed_body = first.replace("Body", "Changed body")
    changed_relation = first.replace("target: project", "target: other-project")
    if canonical_digest(first) != canonical_digest(reordered):
        raise ValueError("digest changed for equivalent YAML/order/line endings")
    if canonical_digest(first) == canonical_digest(changed_body):
        raise ValueError("digest ignored a body change")
    if canonical_digest(first) == canonical_digest(changed_relation):
        raise ValueError("digest ignored a relation change")


def validate_installation_cases() -> None:
    fixture = load_json(ROOT / "tests/fixtures/valid/client-installation.json")
    cases_path = ROOT / "tests/conformance/client-installation-cases.yaml"
    cases = yaml.safe_load(cases_path.read_text(encoding="utf-8"))["cases"]
    manifest = load_manifest()
    for case in cases:
        receipt = json.loads(json.dumps(fixture))
        receipt["previous_installation"] = case["previous"]
        receipt["access_mode"] = case["access_mode"]
        receipt["migration_ready"] = case["migration_ready"]
        if case["checks"] == "handoff-not-run":
            receipt["checks"]["handoff_probe"] = "not-run"
        elif case["checks"] == "safe-read-only":
            receipt["checks"]["proposal_probe"] = "not-applicable"
            receipt["checks"]["conflict_probe"] = "not-applicable"
            receipt["checks"]["handoff_probe"] = "not-run"
        errors = installation_errors(receipt, manifest)
        expected_error = case.get("expected_error")
        if expected_error and not any(expected_error in error for error in errors):
            raise ValueError(f"installation case did not fail as expected: {case['name']}")
        if not expected_error and errors:
            raise ValueError(f"installation case failed: {case['name']}: {errors[0]}")


def main() -> int:
    try:
        schemas, registry = load_schemas()
        validate_fixtures(schemas, registry)
        validate_markdown_links()
        validate_manifest()
        validate_privacy()
        validate_digest_invariants()
        validate_installation_cases()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print("Mind Palace protocol validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
