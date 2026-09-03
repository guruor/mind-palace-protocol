# Migration Preflight

Run this read-only process before any product migration.

## Client Gate

- Validate the active installation receipt and immutable package identity.
- Validate the host-specific adapter declaration and its activation/rollback
  mechanism against `bindings/client-adapter.md`.
- Confirm no previous protocol version retains competing write authority.
- Pass the two-client handoff test when another client may continue the work.
- Confirm the selected methodology and storage binding resolve from the active
  package rather than copied conversation instructions.

## Corpus Gate

- inventory artifacts, properties, hierarchy, relations, links, discussions,
  permissions, icons/covers, embeds, and assets;
- allocate stable IDs and check collisions across the instance;
- classify authority, trust domain, lifecycle, target kind, and canonical source;
- identify unsupported or lossy content before mutation;
- snapshot recoverable content plus storage-only metadata;
- produce source-to-target mapping, rollback, omission report, and canary scope.

## Execution Gate

- prove idempotent reruns do not duplicate artifacts;
- prove interruption can resume from recorded state;
- re-read source identity immediately before every write;
- skip stale artifacts and emit non-canonical conflicts;
- preserve one write authority and serialize writes per artifact;
- require one bounded approval for the reviewed write plan, then continue
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
