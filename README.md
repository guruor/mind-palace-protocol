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

1. Users start with [`INSTALL.md`](INSTALL.md).
2. Maintainers read [`AGENTS.md`](AGENTS.md) before changing the repository.
3. Install or check the shared release using
   [`protocol/common-memory-installation.md`](protocol/common-memory-installation.md).
4. Read [`protocol/general-guide.md`](protocol/general-guide.md) to operate as a
   compatible client.
5. Install or validate the current client using
   [`protocol/client-installation.md`](protocol/client-installation.md).
6. Read the selected methodology, initially
   [`methodologies/product-engineering/README.md`](methodologies/product-engineering/README.md).
7. Read the applicable storage and client adapters under [`bindings/`](bindings/).
8. Run `uv run --frozen scripts/validate.py` before proposing a release or
   migration.

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
the final live OpenCode/hosted-chat gate.

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
