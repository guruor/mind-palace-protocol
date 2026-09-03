# Notion Binding

## Status

Experimental representation contract. Migration is blocked until the targeted
proofs in [`docs/targeted-proofs.md`](../docs/targeted-proofs.md) pass.

## Preferred Representation

Use one Artifact Registry database item as one artifact:

- database properties hold core and query-critical methodology metadata;
- the same item's page body holds document content;
- views may hide machine-oriented properties from normal human navigation;
- native relations may supplement, but never replace, stable artifact IDs.

This avoids maintaining a writable metadata page separately from its content.

## Legacy Bridge

For existing ordinary pages, a registry row may temporarily hold metadata and
link to the page. The bridge must record stable ID, authoritative page locator,
revision, source change token, and relation targets. Validation detects missing
pages and ID, title, revision, relation, or locator drift.

The bridge is migration state, not the target architecture.

## Protocol Installation Registry

Represent shared protocol installation as one full-page registry database in
the configured AI-collaboration/configuration area. Use one item per root,
release, projected component, client receipt, legacy reference, or conflict.
Recommended properties are:

- `Record` (title);
- `Stable ID` (text, unique by validation);
- `Record Type` (installation, release, component, client-receipt, legacy, or
  conflict);
- `Protocol Version`, `Source Version`, `Status`, `Trust Domain`, and `Digest`;
- `Package Locator` when the immutable package is reachable;
- self-relation `Parent Record`/`Child Records`.

The root stable ID defaults to `mind-palace-protocol-installation`. Its active
release is a relation, not copied content. Release components are generated from
the immutable package and carry per-component digests; clients fetch their page
bodies when direct repository access is unavailable. Client receipts and legacy
guidance are related records, so reinstall can upsert them without changing the
legacy page.

Before creating the registry, search both exact stable ID and title. A title
match without the stable ID is an unversioned candidate requiring review, not a
safe upsert target.

## Required Capabilities

The binding must be able to:

- resolve an artifact by stable ID;
- query by kind, methodology, authority, trust domain, and state;
- read properties and body;
- preserve relations and unknown extensions;
- expose page/database locator and last-edited change identity;
- re-read immediately before updates;
- export portable body, metadata, relations, and assets with omission reports.

## Limitations

- `last_edited_at` detects change but is not an immutable content snapshot.
- A pre-write re-read may not provide atomic compare-and-swap. Serialize writes
  per artifact where possible and preserve conflicts when a mismatch appears.
- Comments/discussions are storage-local unless promoted into a durable review,
  decision, or change artifact.
- Database views and UI layout are derived navigation, not canonical content.
- Uploaded-file URLs may expire and must be exported to durable assets.
- Notion-specific blocks require explicit portable mapping or omission; never
  claim lossless GFM conversion without proof.

## Synthetic Proof Evidence

The 2026-09-03 synthetic proof established:

- registry properties can be queried without reading page bodies;
- one database item can hold metadata and body while native relations remain
  queryable;
- moving an ordinary page into the database preserved URL, title, icon, body,
  headings, lists, links, table, code, callout, and page mention;
- moving it back preserved those content elements but removed database-only
  metadata, so rollback requires a metadata snapshot and reapplication plan;
- headings, lists, links, emphasis, inline/fenced code, and tables have direct
  portable-body mappings;
- callouts and page mentions remain Notion-flavored structures and require
  conversion plus stable relation/link preservation;
- an uploaded text attachment was recoverable through the integration-created
  upload identity, but the fetched page used an opaque storage locator, so
  export must copy assets rather than preserve that locator;
- comments/discussions are separately retrievable and can include user identity
  metadata. Export them only when required, minimize/redact identity, and
  promote material conclusions into durable artifacts.

Metadata-first operation and content preservation pass. Human UX, permission
inheritance across representative access boundaries, full asset classes, and
loss-resistant round-trip remain migration gates.

## Safe Failure

If required metadata, permissions, relation targets, export fidelity, or write
conflict checks are unavailable, remain read-only and report the gap. Never
silently flatten or overwrite unsupported semantics.
