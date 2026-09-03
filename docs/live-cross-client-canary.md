# Live OpenCode-To-Hosted-Chat Canary

The local E2E simulation is required but cannot prove host persistence,
connector authorization, tool behavior, or live Notion semantics. Run this
synthetic live canary before production migration.

## Preconditions

- The protocol release is committed/tagged and identified by an immutable Git
  commit or verified package digest.
- OpenCode and the selected hosted-client adapter declare their install,
  discover, activate, validate, and rollback mechanisms under
  `bindings/client-adapter.md`.
- Both clients validate installation receipts for the same protocol and
  methodology release.
- Select ChatGPT or Claude as Client B and use that host's documented adapter.
  Repeat this canary separately before marking another hosted client
  migration-ready.
- A synthetic Notion project contains representative properties, relations,
  headings, lists, links, table, code, mention, callout, discussion, image/PDF,
  and an unsupported-content marker.
- Neither client receives credentials through the protocol package or handoff.

## Phase 1: Independent Resolution

1. Start a new OpenCode session and a new Client B conversation with no shared
   conversation history.
2. Install/resolve the same immutable release using each host's adapter.
3. Validate each installation receipt.
4. Ask each client independently to report protocol/methodology versions,
   instance/trust references, access mode, package source identity, and known
   limitations.
5. Fail if either answer depends on pasted protocol prose, resolves another
   version, or claims knowledge access not provided by its connector.

## Phase 2: Read-Only Handoff

1. OpenCode inventories the synthetic project and emits a handoff conforming to
   `schemas/client-handoff.schema.json`.
2. Give Client B only the handoff plus access to its independently installed
   protocol and authorized Notion connection.
3. Client B validates the handoff, resolves artifacts by stable ID, rechecks
   source identities, and produces a read-only migration map.
4. Compare source counts, classifications, relations, authority, trust domain,
   omissions, and approval scope with OpenCode's map.

## Phase 3: Stale-Source Refusal

1. Change one synthetic source after the handoff.
2. Ask Client B to execute the stale plan.
3. Pass only if it skips the changed artifact, leaves the canonical target
   unchanged, and preserves a non-canonical conflict with base/current evidence.

## Phase 4: Approved Canary And Idempotency

1. OpenCode emits a refreshed handoff for one synthetic artifact.
2. Grant bounded approval for that stable ID and target only.
3. Client B migrates the canary, validates it, and records omissions.
4. Repeat the same request. Pass only if no duplicate page, relation, asset, or
   history entry is created.
5. Verify title, body, properties, relations, source identity/digest,
   permissions, assets, and effective write authority.

## Phase 5: Rollback And Reverse Handoff

1. Execute the reviewed rollback, including database metadata and client
   activation/configuration where applicable.
2. Confirm the pre-canary source/target state and permissions are restored.
3. Have Client B emit a handoff back to a newly initialized OpenCode session.
4. Pass only if OpenCode independently reconstructs the final state, omissions,
   conflict history, and approval boundary.

## Evidence

Record client/version, adapter/version, protocol commit/digest, installation
receipt digests, handoff digests, synthetic artifact IDs, timestamps, checks,
failures/skips, rollback result, and final verdict. Keep private locators and
identity details inside the authorized Mind Palace evidence artifact, never in
this repository.

The verdict is `PASS`, `PARTIAL`, or `FAIL`. A partial or failed canary keeps
production migration disabled but may still authorize a narrower read-only or
proposal-only workflow.
