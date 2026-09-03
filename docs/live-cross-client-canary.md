# Client Setup And Cross-Client Validation

This guide separates client activation from portability and migration testing.
Earlier evidence may call the complete workflow a "live canary"; do not use that
phrase as a test instruction because it does not identify which stage to run.

The deterministic local E2E remains required, but it cannot prove host
persistence, connector authorization, hosted tool behavior, or live Notion
semantics.

## Preconditions

- The protocol release is tagged and identified by an exact Git commit or
  verified package digest.
- Each client uses its declared adapter and an independently authorized
  common-memory connector.
- A synthetic Notion project contains representative metadata, relations, body
  structures, links, discussions, assets, and an unsupported-content marker.
- Neither client receives credentials through the protocol package or handoff.
- Production knowledge remains out of scope until every required stage passes
  and the user grants separate migration approval.

## Stage 1: Fresh-Client Setup Check

Run this separately for every client after its persistent adapter is installed:

```text
Run the Mind Palace Fresh-Client Setup Check. Resolve the installation using
only your persistent adapter and authorized connector, without relying on prior
conversation history or pasted protocol text. Report the active release,
methodology, binding, trust domain, access mode, and limitations. Using only
synthetic content, run the read, bounded-proposal, and stale-source refusal
checks. Do not migrate production knowledge. Update the existing client receipt
rather than creating another one.
```

Pass when the fresh client independently:

- resolves the expected immutable release and configured instance;
- reads the current synthetic artifact by stable ID;
- produces a proposal without mutating the canonical artifact;
- refuses an automatic stale-source write and preserves conflict evidence; and
- records truthful receipt results without claiming the handoff check passed.

A client can pass Stage 1 with `handoff_probe: not-run` and
`migration_ready: false`. That means client setup works; it does not yet prove
cross-client portability.

## Stage 2: Cross-Client Handoff Check

Start a new Client A session and request:

```text
Run the Mind Palace Cross-Client Handoff Check as Client A. Inventory the
synthetic project and emit only a handoff conforming to
schemas/client-handoff.schema.json. Freeze source identities and include scope,
trust domain, omissions, conflicts, and approval state. Do not include
credentials, private document bodies, or hidden conversation context.
```

Give only that handoff to a separately initialized Client B conversation and
request:

```text
Run the Mind Palace Cross-Client Handoff Check as Client B. Use your persistent
adapter and authorized connector to validate this handoff, independently resolve
the active release and every referenced stable artifact ID, recheck source
identities, and produce a read-only migration map. Do not execute writes.
```

Pass when Client B validates the handoff without copied protocol prose or shared
chat history and both clients agree on source counts, classifications,
relations, authority, trust domain, omissions, and approval scope.

## Stage 3: Cross-Client Stale-Source Check

1. Change one synthetic source after Client A emits the handoff.
2. Ask Client B to continue from the now-stale handoff.
3. Pass only if Client B skips the changed artifact, leaves the canonical target
   unchanged, and preserves a non-canonical conflict with base/current evidence.

This check proves stale-source handling across the client boundary. It is
separate from the single-client stale-source check in Stage 1.

## Stage 4: Approved Write Canary And Idempotency

1. Have Client A emit a refreshed handoff for one synthetic artifact.
2. Grant explicit bounded approval for that stable ID and target only.
3. Have Client B migrate the synthetic artifact, validate it, and record
   omissions.
4. Repeat the same request. Pass only if no duplicate page, relation, asset, or
   history entry is created.
5. Verify title, body, properties, relations, source identity/digest,
   permissions, assets, and effective write authority.

"Canary" in this guide means only this one approved synthetic write, not the
entire client-validation workflow.

## Stage 5: Rollback And Reverse Handoff

1. Execute the reviewed rollback, including database metadata and client
   activation/configuration where applicable.
2. Confirm the pre-write source/target state and permissions are restored.
3. Have Client B emit a handoff back to a newly initialized Client A session.
4. Pass only if Client A independently reconstructs the final state, omissions,
   conflict history, and approval boundary.

## Evidence And Verdicts

Record client/version, adapter/version, protocol commit/digest, receipt and
handoff digests, synthetic artifact IDs, timestamps, checks, failures/skips,
rollback result, and stage verdicts. Keep private locators and identity details
inside the authorized Mind Palace evidence artifact, never in this repository.

Record each stage as `PASS`, `PARTIAL`, `FAIL`, or `NOT RUN`. Do not collapse
them into one ambiguous verdict. Production migration remains disabled until
all required stages pass and separate migration approval exists.
