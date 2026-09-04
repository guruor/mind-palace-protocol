# Mind Palace Protocol

Portable contracts for organizing, retrieving, reviewing, updating, and
migrating durable knowledge across AI clients and knowledge stores.

The protocol is storage-neutral. Notion is the first active storage binding;
Markdown plus YAML front matter is the portable representation. Private
knowledge and user configuration do not belong in this repository.

## Status

Version `0.3.0` adds declarative contracts for document types, Knowledge Method
packages, Storage Binding packages, and instance selection. The protocol defines
types rather than tracking individual user documents. Existing Mind Palace
content is not yet migrated, and common memory remains on the active `v0.1.0`
installation.

## Start Here

1. Users start with [`INSTALL.md`](INSTALL.md).
2. Maintainers read [`AGENTS.md`](AGENTS.md) before changing the repository.
3. Install or check the shared release using
   [`protocol/common-memory-installation.md`](protocol/common-memory-installation.md).
4. Read [`protocol/general-guide.md`](protocol/general-guide.md) to operate as a
   compatible client.
5. Install the current client's version-neutral discovery adapter once using
   [`protocol/client-installation.md`](protocol/client-installation.md).
6. Read the selected methodology, initially
   [`methodologies/product-engineering/README.md`](methodologies/product-engineering/README.md).
7. Read the applicable storage and client adapters under [`bindings/`](bindings/).
8. Run `uv run --frozen scripts/validate.py` before proposing a release or
   migration.

Use [`docs/extension-authoring.md`](docs/extension-authoring.md) to understand
the declarative method and binding contracts. External package resolution is
not enabled until the later custom-package release.

Calculate a frozen artifact digest with
`uv run --frozen scripts/digest.py <artifact.md>`.

Validate an installed client's receipt with
`uv run --frozen scripts/validate_installation.py <receipt.json>`.

Validate a cross-client handoff with
`uv run --frozen scripts/validate_handoff.py <handoff.json>`.

Run the deterministic two-client migration scenario with
`uv run --frozen scripts/e2e_cross_client.py`.

Run shared-installation and non-destructive client-configuration cases with
`uv run --frozen scripts/common_memory_install.py` and
`uv run --frozen scripts/client_adapter_config.py`.

Use [`docs/live-cross-client-canary.md`](docs/live-cross-client-canary.md) for
the Fresh-Client Setup Check, Cross-Client Handoff Check, approved write canary,
and rollback stages.

## Layout

- `protocol/`: generic client behavior and protocol release metadata.
- `schemas/`: portable JSON Schema contracts.
- `methodologies/`: built-in Knowledge Methods and document-type rules.
- `bindings/`: built-in Storage Bindings and client capability contracts.
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
