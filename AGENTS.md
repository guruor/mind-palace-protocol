# Agent Instructions

This repository is designed to be maintained by humans and AI agents.

## Required Context

1. Read `README.md`, `docs/architecture.md`, `docs/contributing.md`, and
   `docs/security-privacy.md` before structural changes.
2. Read `protocol/general-guide.md` before changing client behavior.
3. Read the owning methodology and binding before changing their artifacts.

## Ownership

- `protocol/` and `schemas/artifact.schema.json` own universal semantics.
- `methodologies/<name>/` owns domain-specific artifacts and lifecycle.
- `bindings/` owns storage-specific representation and limitations.
- `examples/` and `tests/` prove behavior; they do not define it.

Maintain each rule once. Reference generic guidance instead of copying it into
methodologies, templates, or bindings. Templates must remain self-explanatory
for their own fields and sections.

## Safety And Portability

- Never commit private notes, raw conversations, credentials, private URLs,
  personal identifiers, or production fixtures.
- Treat protocol access and knowledge access as separate authorization.
- Keep stable identity independent of Notion IDs, URLs, and Git paths.
- Keep portable semantics independent of Notion, GitHub, OpenCode, ChatGPT, or
  another vendor. Bindings may use native features without changing meaning.
- Preserve unknown extension fields during read-modify-write and round trips.
- Do not silently overwrite conflicts, broaden a trust domain, or migrate
  existing knowledge.
- Do not add another methodology, storage binding, index, synchronization
  service, or orchestration framework without an approved concrete use case.

## Change Process

- Prefer the smallest compatible change.
- Update architecture before material structural changes.
- Use Semantic Versioning for released protocol and methodology contracts;
  protocol `0.y.z` remains unstable during the pilot.
- Add deterministic fixtures for schema or compatibility changes.
- Run `uv run --frozen scripts/validate.py` and review the final diff.
- Migration requires a reviewed source-to-target map, recoverable snapshot,
  validation plan, and explicit approval.
