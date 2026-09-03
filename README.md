# Mind Palace Protocol

Portable contracts for organizing, retrieving, reviewing, updating, and
migrating durable knowledge across AI clients and knowledge stores.

The protocol is storage-neutral. Notion is the first active storage binding;
Markdown plus YAML front matter is the portable representation. Private
knowledge and user configuration do not belong in this repository.

## Status

Version `0.1.0` is an initial implementation of the approved architecture. It
defines the general guide, portable artifact envelope, the first
`product-engineering` methodology, binding contracts, examples, and
deterministic validation. Existing Mind Palace content is not yet migrated.

## Start Here

1. Read [`AGENTS.md`](AGENTS.md) before changing the repository.
2. Read [`protocol/general-guide.md`](protocol/general-guide.md) to operate as a
   compatible client.
3. Install or validate a client using
   [`protocol/client-installation.md`](protocol/client-installation.md).
4. Read the selected methodology, initially
   [`methodologies/product-engineering/README.md`](methodologies/product-engineering/README.md).
5. Read the applicable storage binding under [`bindings/`](bindings/).
6. Run `uv run --frozen scripts/validate.py` before proposing a release or
   migration.

Calculate a frozen artifact digest with
`uv run --frozen scripts/digest.py <artifact.md>`.

Validate an installed client's receipt with
`uv run --frozen scripts/validate_installation.py <receipt.json>`.

## Layout

- `protocol/`: generic client behavior and protocol release metadata.
- `schemas/`: portable JSON Schema contracts.
- `methodologies/`: domain-specific lifecycle, artifact, and template rules.
- `bindings/`: storage representation and capability contracts.
- `examples/`: non-sensitive representative portable artifacts.
- `tests/fixtures/`: deterministic valid and invalid schema cases.
- `tests/conformance/`: executable client and compatibility case definitions.
- `scripts/`: repository validation.
- `docs/`: architecture, contribution, security, and proof plans.

## Authority

This repository is authoritative for released protocol behavior and schemas.
A configured Mind Palace instance is authoritative for its approved intent and
knowledge. A software repository remains authoritative for its implementation,
configuration, and validation evidence.
