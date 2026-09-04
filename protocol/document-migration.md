# Document Migration

## User Request

A user may ask a compatible client to migrate named documents, a container, or
all documents in an authorized Mind Palace boundary. The request authorizes a
read-only preflight, not migration writes.

Interpret scope narrowly:

- `selected` means only the named documents plus dependencies that must be read
  to understand identity, relationships, permissions, or active baselines;
- `all-authorized` means every document discoverable inside the explicitly
  authorized boundary, never the whole provider account or another trust domain;
- report dependency reads and exclusions separately from proposed write scope;
- ask one focused scope question only when the requested boundary cannot be
  resolved safely.

## Preflight

Resolve the active protocol, Knowledge Method, Storage Binding, trust domain,
and executing client's receipt. Inventory source bodies, metadata, hierarchy,
relations, links, comments, permissions, icons/covers, embeds, and assets using
the minimum access needed.

For each source, record:

- stable source identity, locator, and current change token or revision;
- authority, trust domain, lifecycle, and active-baseline role;
- classification as `conformant`, `partial`, `legacy`, `duplicate`, `unknown`,
  or `out-of-scope`;
- target document type or an explicit retained/omitted disposition;
- unsupported content, information-loss risk, unresolved permissions, and
  relation dependencies.

## AI-Assisted Conversion

AI may transform a source into the target document type when the plan records
the exact transformation and semantic impact:

- `preserve`: copy content without rewriting meaning;
- `structural`: add portable metadata, normalize headings, move intact sections,
  or convert equivalent formatting;
- `meaning-preserving`: clarify wording or merge clear redundancy while retaining
  facts, uncertainty, rationale, history, decisions, and scope;
- `material`: change, remove, infer, or promote meaning;
- `unknown`: impact cannot be established confidently.

Structural and low-impact meaning-preserving transformations may execute after
the user approves the exact plan and representative before/after preview.
Material or unknown impact must be highlighted separately and acknowledged in
the approval. Never rewrite append-only history, invent missing decisions,
convert hypotheses into facts, or let technical intent impersonate verified
implementation truth.

Do not create missing documents for symmetry. Preserve unknown extensions and
distinguish current intent, implementation truth, evidence, history, and
configuration.

## Reviewed Plan

Produce a plan conforming to `schemas/migration-plan.schema.json`. It must show:

1. requested, read-only dependency, excluded, and proposed write scopes;
2. source-to-target mapping and per-document action;
3. expected base revision for every source that may be changed;
4. stable-ID allocation and collision checks;
5. information-loss, permission, asset, relation, and active-baseline risks;
6. provider-aware records, bytes, attachments, requests, batches, delays,
   retries, reserved request headroom, checkpoint frequency, and rollback cost;
7. snapshots, rollback order, validation, omissions, and unresolved blockers.

The first plan state is `draft` with approval `pending`. A request such as
"migrate these documents" or "migrate everything" does not approve the plan it
produces.

## Confirmation

Present one concrete decision using the General Guide's Decision Questions
format. Identify the exact plan ID, scope digest, documents and actions, known
loss or ambiguity, write budget, rollback, and anything intentionally retained.
Ask the user to approve that plan or request changes.

Approval applies only to the reviewed scope digest and base revisions. Re-plan
instead of writing when scope, source state, permissions, loss, target method,
storage binding, budget, or rollback changes materially.

## Execution

After approval:

1. re-read each source immediately before its write;
2. skip stale sources and preserve a non-canonical conflict;
3. execute serialized, bounded, idempotent batches;
4. persist completed stable IDs so interrupted work resumes without duplication;
5. keep one write authority and preserve active delivery baselines;
6. stop on an unapproved ambiguity, permission change, loss, or budget breach.

## Incremental And Rate-Limited Execution

Prefer a slow successful migration to a large fragile run. Default to one
document per execution batch unless the reviewed provider evidence safely
supports more.

- reserve request capacity for verification and rollback instead of planning to
  the provider maximum;
- checkpoint completed stable IDs after every document by default;
- on rate limiting, stop new writes, honor `Retry-After` or the configured
  fallback, persist `paused-rate-limit`, and resume only pending work;
- cap retry attempts and require a new plan when the provider repeatedly rejects
  the same operation;
- do not roll back already validated documents merely because a later batch is
  paused; roll back only the affected approved scope when required;
- re-read source and target state after a pause before resuming;
- allow the user to stop safely between batches without converting that pause
  into migration failure.

Approval does not authorize access outside the trust boundary, deletion of
unlisted sources, cleanup of legacy records, or a methodology/configuration
change not present in the plan.

## Validation And Completion

Compare source and target counts, stable IDs, bodies, revisions/digests,
relations, links, authority, trust boundaries, permissions, assets, and
omissions. Run the approved canary before the remaining scope when the binding
or content class lacks representative evidence.

Mark the plan `completed` only after validation passes. Otherwise mark it
`blocked`, keep recoverable evidence, and execute the reviewed rollback when
needed. Record results without copying private document content into the public
protocol repository.
