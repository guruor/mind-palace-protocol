# Common-Memory Installation

## User Experience

The user explicitly asks a capable client to **install Mind Palace protocol** or
**update Mind Palace protocol** and provides or confirms the common-memory
destination. Protocol installation and update are manual operations: normal
Mind Palace work must never discover or activate a newer release automatically.
The agent performs the requested common-memory operation:

1. install, update, repair, or validate the protocol release in common memory;
2. leave every already-installed version-neutral client adapter unchanged.

The agent asks only when authorization, an incompatible upgrade, an ambiguous
legacy installation, or a host setting cannot be completed safely. A successful
common-memory installation can be reused by every authorized client. Each
client needs its thin discovery adapter only once and keeps at most one receipt
with its latest recorded release and capability evidence.

## Common-Memory Records

Create or resolve one root record by stable installation ID, never by title
alone. The root contains:

- active immutable release pointer;
- one latest active Source Pointer after successful activation;
- only explicitly exempted non-protocol legacy references;
- links to client installation receipts;
- actual storage binding and trust domain.

Unless instance configuration overrides it, use stable installation ID
`mind-palace-protocol-installation` and human title
`Mind Palace Protocol Installation`.

Each release comes from one immutable protocol package. A staged release record
stores only its version, immutable package locator, source revision, Release
Index digest, trust domain, and relation to the installation root. It does not
copy or attach protocol resources. Clients fetch the Release Index and required
resources from that immutable source and verify their declared digests.

Fetch `core` resources for normal protocol work and `on-demand` resources only
when a task needs them. Verify the immutable release revision and digest before
use. A verified resource may enter a runtime-local disposable cache, never a
provider-backed protocol record. Cache failure must not block read or proposal
work.
Fetch `maintenance` resources only for an explicit maintenance operation. Never
place `development` resources in common memory.

Rollback recreates a Source Pointer from an immutable prior repository release.
It does not require retaining prior protocol records in common memory.

## Write Plan

Before any staging, repair, cache, rollback, or cleanup write, create a read-only
plan. Report records, text bytes, attachments, requests, batch size, delays,
retry limits, cache impact, and rollback writes. Reuse existing records and
reject the plan before its first write when any configured provider budget is
exceeded.

Bind approval to the source revision, Release Index digest, target stable ID,
operations, validation, and rollback. Verify the Release Index and all required
core-resource digests directly from the immutable source before staging.

Writes use bounded batches and persist completed stable IDs. On a rate limit,
stop new writes, honor the provider retry delay or the configured fallback,
re-read current state, and resume only missing work. Never move the active
release pointer until staged validation and explicit approval pass. Cache
failure does not block read or proposal work.

## Install Or Check

1. Search the authorized common-memory boundary for the stable installation ID.
2. If absent, create the root and candidate release with an inactive write
   surface, validate it, then set the active pointer.
3. If the same version and immutable package identity exists, verify the Source
   Pointer and return `no-op`; never create or repair copied protocol resources.
4. If the same version has another package identity or a component digest
   differs, do not overwrite it. Record a conflict and remain on the current
   release.
5. Only after an explicit update request, if the candidate is newer, create it
   as `staged`. During `0.y.z`, assess compatibility explicitly. Activate after
   source validation and required approval. After the required client-resolution
   check passes, remove superseded protocol releases and components. Do not
   require unrelated document migrations before protocol activation.
6. If the candidate is older, do not downgrade automatically.
7. Preserve only legacy/unversioned instruction sources explicitly exempted by
   the user. Remove superseded protocol records after replacement validation.
8. Validate `schemas/common-memory-installation.schema.json`, active-pointer
   uniqueness, stable IDs, index and core digests, trust boundary, and
   permissions.

Read the staged record back before activation and verify its exact properties.
Fetch the Release Index from the immutable package locator, verify its digest,
then fetch and verify every required core resource. If identity, availability,
bytes, or digest differs, mark only the candidate blocked and leave the active
pointer unchanged.

After successful activation and client-resolution validation, cleanup is
automatic and resumable: remove all older protocol release and component
records from the installation map in provider-bounded batches. Preserve the
installation root, client receipts, user documents, and explicitly exempted
legacy guidance. When the provider cannot permanently delete records, remove
them from active discovery and report the exact manual deletion list.

## Idempotency

The idempotency key is:

```text
installation_id + protocol_version + immutable_package_identity
```

The installer uses upsert-by-stable-ID semantics. It never creates another root
or release for the same key, never appends duplicate client receipts, and never
rewrites user-maintained content. A retry after interruption resumes the staged
release and missing core resources.

## Client Discovery

For a client's first setup, select its host adapter. The adapter adds a small,
version-neutral bootstrap reference through a host-native additive mechanism.
It must not copy the protocol into an existing instruction file, pin a release,
or replace user/system instructions. The bootstrap tells the client when and
how to resolve the active common-memory installation; the release projection
remains the behavior source.

Create one client receipt by stable client/installation identity and run setup
probes. On later protocol updates, do not reinstall or edit the adapter. The
client resolves the new active release on its next Mind Palace operation,
validates compatibility, and follows it without changing client configuration.
Receipt refresh is required before protocol-governed writes or when explicitly
requested, not as a side effect of an ordinary read. If resolution fails, the
client remains read-only and reports the mismatch; it does not roll back common
memory or silently use a different release.

## Validation

The deterministic common-memory scenario covers first install, exact rerun,
missing-component repair, same-version identity conflict, staged upgrade,
approved activation, downgrade refusal, legacy preservation, receipt
deduplication, and rollback:

```sh
uv run --frozen scripts/common_memory_install.py
uv run --frozen scripts/common_memory_plan.py --source-revision COMMIT
```
