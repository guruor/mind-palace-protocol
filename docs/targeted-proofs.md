# Targeted Proof Plan

The architecture is approved, but migration remains blocked on four bounded
proofs.

## P1: Notion Representation

Compare an Artifact Registry database item whose properties and body form one
artifact with a temporary registry row linked to an ordinary page. Verify
content, links, permissions, navigation, visual noise, metadata-first query,
move behavior, and rollback.

Partial pass on 2026-09-03 with synthetic content: metadata-first query, native
relation, database-item body, move, and content rollback succeeded. Database
properties were removed when moving back to an ordinary parent, proving that a
rollback requires a metadata snapshot/reapply step. Human UX and permission
inheritance remain unverified.

## P2: Portable Round Trip

Exercise headings, lists, tables, code, links, mentions, relations, child-page
references, comments/discussions, and uploaded assets. Classify each as
portable body, structured metadata/relation, exported asset, storage-local
provenance, or unsupported/blocking. Do not claim lossless conversion without
evidence.

Partial pass on 2026-09-03: standard text structures round-tripped through the
Notion MCP representation. Callout, page mention, discussion, and attachment
evidence confirmed that explicit conversion, redaction, and asset export are
required. Full Markdown export/import and binary asset coverage remain pending.

## P3: Conflict Handling

Create two proposals from one base revision. Apply one, then prove the second
cannot overwrite it silently and is preserved as a conflict artifact. Record
whether the Notion binding can provide atomic compare-and-swap; otherwise test
serialized writes plus immediate pre-write verification.

Process pass on 2026-09-03: Proposal A advanced a synthetic artifact from
revision 1 to 2; stale Proposal B was not applied and was preserved as a
non-canonical conflict artifact. Atomic compare-and-swap remains unavailable in
the current proof surface, so V1 must serialize writes per artifact and re-read
immediately before mutation.

## P4: Digest Normalization

Define canonical serialization for core metadata, methodology metadata, and
portable body. Prove harmless storage formatting does not change the digest
while meaningful metadata, relation, or body changes do.

Implemented in [`digest-normalization.md`](digest-normalization.md) and
`scripts/digest.py`; deterministic invariants run in repository validation.

Each proof records setup, evidence, result, limitations, verdict, and cleanup.
Use only synthetic non-sensitive fixtures.
