# Migration Preflight Validation Profile

The canonical user-facing workflow is
[`protocol/document-migration.md`](../protocol/document-migration.md). This
document defines the additional evidence required before maintainers claim that
a storage/client combination is ready for real migration.

## Client Gate

- Resolve the active release through the stable common-memory root. Do not
  install or update the shared protocol as a side effect of document migration.
- Validate the active installation receipt and immutable package identity.
- Validate the host-specific adapter declaration and its activation/rollback
  mechanism against `bindings/client-adapter.md`.
- Confirm no previous protocol version retains competing write authority.
- Pass the Fresh-Client Setup Check for the executing client's one-time adapter
  setup and the approved write canary before its first real migration.
- Pass the Cross-Client Handoff Check only when another client may continue or
  independently execute part of the work. Do not make cross-client validation a
  universal gate for a single-client migration.
- Confirm the selected methodology and storage binding resolve from the active
  package rather than copied conversation instructions.

## Corpus Gate

- validate that the generated migration plan contains the complete inventory,
  mapping, risks, snapshots, omissions, provider budget, and approval boundary;
- verify `selected` and `all-authorized` scopes do not cross trust domains;
- verify dependency reads are not silently promoted into write scope;
- verify stable-ID collisions and unsupported content block execution.

## Execution Gate

- prove idempotent reruns do not duplicate artifacts;
- prove interruption can resume from recorded state;
- re-read source identity immediately before every write;
- skip stale artifacts and emit non-canonical conflicts;
- preserve one write authority and serialize writes per artifact;
- require one bounded approval tied to the plan scope digest and base revisions,
  then continue
  automatically unless a new ambiguity, permission change, loss, or conflict
  exceeds that scope.

## Validation Gate

- compare counts, stable IDs, revisions/digests, relations, links, authority,
  trust boundaries, and omissions;
- verify effective permissions did not broaden or unexpectedly narrow;
- verify binary assets through at least an image or PDF case;
- validate human navigation/visual noise on a canary batch;
- prove rollback restores body, hierarchy, properties, relations, and assets;
- retain migration evidence without copying private content into this protocol
  repository.

## Rollout Sequence

1. Mind Palace read-only preflight and synthetic/canary migration.
2. Mind Palace bounded migration after approval and gate completion.
3. Agent Workspace as the second portability pilot.
4. Additional product documentation only after both pilots pass.

For Agent Workspace, repository files remain implementation truth. Notion may
hold intent, decisions, evidence, or repository references, but must not become
a second writable copy of canonical agent definitions, Skills, standards, or
runtime configuration.
