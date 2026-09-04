# Product Engineering Migration

Migration follows the protocol-wide
[`Document Migration`](../../../protocol/document-migration.md) workflow. It is
explicit and approval-gated and never runs as a side effect of selecting this
Knowledge Method.

## Required Plan

1. Record the source method, version, storage, and immutable source snapshot.
2. Inventory document types, metadata, sections, relations, assets, and access.
3. Map every source document type and field to this method or list it as an
   omission with impact.
4. Protect active delivery baselines and current implementation work.
5. Define rollback and validation before writing.
6. Run one bounded canary, verify it, and obtain approval for the remaining
   reviewed scope.

AI-assisted conversion may normalize metadata, headings, equivalent formatting,
and section placement when the reviewed plan classifies semantic impact as none
or low. Preserve product behavior, technical constraints, uncertainty, accepted
history, rationale, and baseline scope. Material or uncertain changes require
explicit acknowledgement in the plan approval.

Preserve stable IDs, provenance, authority, history, relations, and unknown
extensions. Do not create empty documents merely to match the catalog.
