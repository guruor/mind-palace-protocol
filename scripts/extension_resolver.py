#!/usr/bin/env python3
"""Resolve one approved declarative extension package safely."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import socket
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
MAX_MANIFEST_BYTES = 200 * 1024
DECLARATIVE_SUFFIXES = {".csv", ".d2", ".drawio", ".json", ".md", ".mmd", ".svg", ".yaml", ".yml"}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def version_tuple(version: str) -> tuple[int, int, int]:
    major, minor, patch = version.split("-", 1)[0].split("+", 1)[0].split(".")
    return int(major), int(minor), int(patch)


def compatible(version: str, requirement: str) -> bool:
    current = version_tuple(version)
    for clause in requirement.split():
        if clause.startswith(">="):
            if current < version_tuple(clause[2:]):
                return False
        elif clause.startswith("<"):
            if current >= version_tuple(clause[1:]):
                return False
        else:
            raise ValueError(f"unsupported protocol requirement: {clause}")
    return True


def validate_schema(value: dict[str, Any], schema_name: str) -> None:
    schemas = []
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas.append((schema["$id"], Resource.from_contents(schema)))
    registry = Registry().with_resources(schemas)
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, registry=registry).iter_errors(value))
    if errors:
        raise ValueError(f"invalid {schema['title']}: {errors[0].message}")


def fetch_https(locator: str) -> bytes:
    parsed = urlparse(locator)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("extension manifest must use HTTPS")
    if parsed.hostname == "localhost" or parsed.hostname.endswith(".local"):
        raise ValueError("extension manifest cannot use a local host")
    for address in socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM):
        if ipaddress.ip_address(address[4][0]).is_private:
            raise ValueError("extension manifest cannot use a private network address")
    request = Request(locator, headers={"User-Agent": "mind-palace-protocol"})
    with build_opener(NoRedirect).open(request, timeout=30) as response:
        payload = response.read(MAX_MANIFEST_BYTES + 1)
    if len(payload) > MAX_MANIFEST_BYTES:
        raise ValueError("extension manifest exceeds 200 KiB")
    return payload


def resolve_extension(
    reference: dict[str, Any],
    protocol_version: str,
    fetcher: Callable[[str], bytes],
    installed_packages: set[str] | None = None,
    document_owners: dict[str, str] | None = None,
    required_capabilities: set[str] | None = None,
) -> dict[str, Any]:
    validate_schema(reference, "extension-source.schema.json")
    if not reference.get("approval_reference"):
        raise ValueError("extension source requires explicit approval")
    payload = fetcher(reference["manifest"]["locator"])
    digest = f"sha256:{hashlib.sha256(payload).hexdigest()}"
    if digest != reference["manifest"]["digest"]:
        raise ValueError("extension manifest digest mismatch")
    package = yaml.safe_load(payload)
    if not isinstance(package, dict):
        raise ValueError("extension manifest must be an object")
    schema_name = "knowledge-method.schema.json" if package.get("kind") == "knowledge-method" else "storage-binding.schema.json"
    validate_schema(package, schema_name)
    for field in ("id", "kind", "version"):
        if package.get(field) != reference.get(field):
            raise ValueError(f"extension {field} does not match approved reference")
    source = package.get("source", {})
    if source.get("type") != "remote" or source.get("revision") != reference["manifest"]["revision"]:
        raise ValueError("extension source revision does not match approved reference")
    if not compatible(protocol_version, package["requires"]["protocol"]):
        raise ValueError("extension is incompatible with the active protocol")
    installed = installed_packages or set()
    missing = set(package["requires"].get("packages", [])) - installed
    if missing:
        raise ValueError(f"extension dependencies are unavailable: {sorted(missing)}")
    for resource in package["resources"]:
        suffix = Path(resource["path"]).suffix.lower()
        if suffix not in DECLARATIVE_SUFFIXES:
            raise ValueError(f"extension contains a non-declarative resource: {resource['path']}")
    owners = document_owners or {}
    for document_type in package.get("provides", {}).get("document_types", []):
        owner = owners.get(document_type)
        if owner and owner != package["id"]:
            raise ValueError(f"document type already belongs to {owner}: {document_type}")
    if package["kind"] == "storage-binding":
        provided = set(package["provides"]["capabilities"])
        missing_capabilities = (required_capabilities or set()) - provided
        if missing_capabilities:
            raise ValueError(f"binding capabilities are unavailable: {sorted(missing_capabilities)}")
    return package


def run_scenario() -> None:
    method_path = ROOT / "examples/extensions/research-method/method.yaml"
    payload = method_path.read_bytes()
    package = yaml.safe_load(payload)
    reference = {
        "id": package["id"],
        "kind": package["kind"],
        "version": package["version"],
        "manifest": {
            "locator": package["source"]["locator"],
            "revision": package["source"]["revision"],
            "digest": f"sha256:{hashlib.sha256(payload).hexdigest()}",
        },
        "approval_reference": "synthetic-approval",
    }
    fetcher = lambda locator: payload
    resolved = resolve_extension(reference, "0.7.0", fetcher)
    if resolved["id"] != "example/research":
        raise ValueError("approved extension did not resolve")

    changed = json.loads(json.dumps(reference))
    changed["manifest"]["digest"] = "sha256:" + "0" * 64
    try:
        resolve_extension(changed, "0.7.0", fetcher)
    except ValueError:
        pass
    else:
        raise ValueError("changed extension content was accepted")

    try:
        resolve_extension(reference, "0.6.0", fetcher)
    except ValueError:
        pass
    else:
        raise ValueError("incompatible extension was accepted")

    try:
        resolve_extension(
            reference,
            "0.7.0",
            fetcher,
            document_owners={"example-research/research-note": "other/method"},
        )
    except ValueError:
        pass
    else:
        raise ValueError("duplicate document type ownership was accepted")

    missing_dependency = json.loads(json.dumps(package))
    missing_dependency["requires"]["packages"] = ["example/missing@0.1.0"]
    dependency_payload = yaml.safe_dump(missing_dependency, sort_keys=False).encode()
    dependency_reference = json.loads(json.dumps(reference))
    dependency_reference["manifest"]["digest"] = f"sha256:{hashlib.sha256(dependency_payload).hexdigest()}"
    try:
        resolve_extension(dependency_reference, "0.7.0", lambda locator: dependency_payload)
    except ValueError:
        pass
    else:
        raise ValueError("extension with a missing dependency was accepted")

    executable = json.loads(json.dumps(package))
    executable["resources"].append(
        {"path": "install.py", "class": "maintenance", "cache": "never", "purpose": "Unsafe executable."}
    )
    executable_payload = yaml.safe_dump(executable, sort_keys=False).encode()
    executable_reference = json.loads(json.dumps(reference))
    executable_reference["manifest"]["digest"] = f"sha256:{hashlib.sha256(executable_payload).hexdigest()}"
    try:
        resolve_extension(executable_reference, "0.7.0", lambda locator: executable_payload)
    except ValueError:
        pass
    else:
        raise ValueError("extension with executable content was accepted")

    binding_path = ROOT / "examples/extensions/plain-files-binding/binding.yaml"
    binding_payload = binding_path.read_bytes()
    binding = yaml.safe_load(binding_payload)
    binding_reference = {
        "id": binding["id"],
        "kind": binding["kind"],
        "version": binding["version"],
        "manifest": {
            "locator": binding["source"]["locator"],
            "revision": binding["source"]["revision"],
            "digest": f"sha256:{hashlib.sha256(binding_payload).hexdigest()}",
        },
        "approval_reference": "synthetic-approval",
    }
    resolved_binding = resolve_extension(
        binding_reference,
        "0.7.0",
        lambda locator: binding_payload,
        required_capabilities={"markdown", "yaml-front-matter"},
    )
    if resolved_binding["kind"] != "storage-binding":
        raise ValueError("approved binding did not resolve")
    try:
        resolve_extension(
            binding_reference,
            "0.7.0",
            lambda locator: binding_payload,
            required_capabilities={"native-relations"},
        )
    except ValueError:
        pass
    else:
        raise ValueError("binding with missing capabilities was accepted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="approved extension-source JSON")
    parser.add_argument("--protocol-version", required=True)
    args = parser.parse_args()
    try:
        reference = json.loads(args.reference.read_text(encoding="utf-8"))
        package = resolve_extension(reference, args.protocol_version, fetch_https)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"extension resolution failed: {exc}")
        return 1
    print(json.dumps({"id": package["id"], "kind": package["kind"], "version": package["version"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
