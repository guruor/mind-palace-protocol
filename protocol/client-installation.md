# Client Installation And Upgrade

## Purpose

Install one immutable protocol release into a client without copying or forking
its rules. A client installation grants protocol capability, not access to a
Mind Palace instance.

The default user flow first runs the shared install/check in
[`common-memory-installation.md`](common-memory-installation.md), then activates
the current client through its declared adapter. If common memory already has
the exact release, the first phase is a no-op or repair and client setup
continues.

The canonical package is the release identified by the installation receipt.
Client-specific adapters store only an activation pointer, authorized instance
references, capabilities, and validation evidence.

## Installation Inputs

- immutable protocol package locator and source version or package digest;
- requested protocol version;
- client and client-adapter identity;
- authorized instance reference and trust domain;
- selected storage binding and methodology versions;
- requested access mode: `read`, `propose`, or `update`.

From the user's perspective, the normal command is simply **Install Mind Palace
protocol**. The agent discovers the destination/release when safely configured,
reports any previous or legacy installation, and asks only for missing access or
a decision that changes active behavior.

Never put credentials, tokens, private document bodies, or unrestricted
production exports in an installation receipt.

## Preflight

Before changing client configuration:

1. Discover every existing protocol pointer, copied guide, retained bootstrap,
   installation receipt, and client-specific adapter configuration.
2. Classify the prior state as `absent`, `same`, `older-compatible`,
   `older-migration-required`, `newer`, `unversioned`, or `invalid`.
3. Snapshot the current activation/configuration within its authorized boundary.
4. Validate the candidate package, release identity, required guides, schemas,
   methodology, and binding.
5. Produce the proposed resolution and its rollback before activation.

Discovery must not delete or overwrite a previous installation. An unversioned
guide is evidence to classify, not permission to replace it.

## Prior-Version Decisions

- `absent`: install normally.
- `same`: require the same immutable package identity, then validate and repair
  only missing adapter state; otherwise no-op. Equal version labels with
  different package identities are invalid and must not replace each other.
- `older-compatible`: activate only after validating compatibility and client
  conformance. Preserve the previous pointer for rollback.
- `older-migration-required`: present the migration impact and obtain approval
  before changing active behavior or persisted configuration.
- `newer`: do not downgrade automatically. Use the newer compatible release,
  install the requested release in parallel, or obtain explicit downgrade
  approval.
- `unversioned`: retain it, map its behavior to the candidate release, report
  conflicts, and obtain approval before replacement. A parallel read-only
  installation is preferred when behavior cannot be mapped safely.
- `invalid`: remain read-only and repair or isolate the installation before use.

During protocol `0.y.z`, every version change receives an explicit compatibility
assessment because minor releases may be incompatible. From `1.0.0`, normal
Semantic Versioning rules apply unless release migration notes say otherwise.

Legacy bootstrap material remains available until the new installation passes
resolution and handoff tests. Do not allow both versions to claim write
authority for the same instance.

## Staged Activation

1. Stage the immutable package without modifying the active pointer.
2. Run package and installation-receipt validation.
3. Resolve the General Guide, selected methodology, and binding from the staged
   package.
4. In a fresh client session, run trust-isolation, read, proposal, and conflict
   probes using synthetic or explicitly authorized content.
5. Record the results in an installation receipt conforming to
   `schemas/client-installation.schema.json`.
6. Activate the staged pointer atomically when the client supports it; otherwise
   use a reversible adapter-specific operation.
7. Repeat resolution and read probes through the active client surface.
8. Run the separate cross-client handoff check with two independently
   initialized clients.
9. Mark migration readiness only when every required gate passes.

On failure, restore the prior pointer/configuration and keep failure evidence.
Never leave a partially validated installation with update authority.

## Cross-Client Handoff

A handoff proves that another compatible client can continue without hidden
conversation state. Client A emits only:

- protocol and methodology versions;
- instance and trust-domain references;
- requested task and access mode;
- stable artifact IDs and frozen revisions/source identities;
- unresolved omissions, conflicts, and approval state.

Client B independently resolves the installed release and authorized instance,
rechecks current source identities, and continues or safely refuses. The handoff
does not embed credentials or grant additional access.

Use these validation names in user-facing instructions:

- **Fresh-Client Setup Check:** prove one newly initialized client resolves its
  persistent adapter and safely runs read/proposal/conflict probes.
- **Cross-Client Handoff Check:** prove independently initialized clients can
  exchange and consume a schema-valid handoff without hidden chat state.
- **Approved Write Canary:** migrate one explicitly approved synthetic artifact,
  prove idempotency, and roll it back.

Do not use "live canary" alone because it does not identify which check the
client should execute.

## Required Validation

`migration_ready: true` requires update access and passing results for package
integrity, protocol/methodology/binding resolution, trust isolation, read,
proposal, conflict, and handoff probes. A failed or unrun required check keeps
the client read-only for migration.

Run:

```sh
uv run --frozen scripts/validate_installation.py <installation-receipt.json>
```
