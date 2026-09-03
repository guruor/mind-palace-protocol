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
- staged, active, retired, and blocked releases;
- generated release components and their digests;
- retained legacy installation references and dispositions;
- links to client installation receipts;
- actual storage binding and trust domain.

Unless instance configuration overrides it, use stable installation ID
`mind-palace-protocol-installation` and human title
`Mind Palace Protocol Installation`.

Each release projection is generated from one immutable protocol package. It is
not edited independently. Store enough readable projected guidance for clients
that cannot access the source repository, plus the package locator, source
identity, component digests, and omission report. Schemas or bundles may be
attached when the storage/client cannot read them inline.

## Install Or Check

1. Search the authorized common-memory boundary for the stable installation ID.
2. If absent, create the root and candidate release with an inactive write
   surface, validate it, then set the active pointer.
3. If the same version and immutable package identity exists, verify component
   digests and references. Return `no-op`, or repair only missing generated
   components and return `repaired`.
4. If the same version has another package identity or a component digest
   differs, do not overwrite it. Record a conflict and remain on the current
   release.
5. Only after an explicit update request, if the candidate is newer, create it
   as `staged`. During `0.y.z`, assess compatibility explicitly. Activate after
   package/projection validation and required approval, retaining the prior
   release for rollback. Do not require unrelated document migrations or every
   client to pass a cross-client handoff before protocol activation.
6. If the candidate is older, do not downgrade automatically.
7. Preserve every legacy/unversioned instruction source. Record whether it is
   retained read-only, mapped, superseded, or blocked; removal requires explicit
   approval after all clients resolve the replacement.
8. Validate `schemas/common-memory-installation.schema.json`, active-pointer
   uniqueness, stable IDs, component digests, trust boundary, and permissions.

## Idempotency

The idempotency key is:

```text
installation_id + protocol_version + immutable_package_identity
```

The installer uses upsert-by-stable-ID semantics. It never creates another root
or release for the same key, never appends duplicate client receipts, and never
rewrites user-maintained content. A retry after interruption resumes the staged
release and missing generated components.

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
```
