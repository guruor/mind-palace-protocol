# Product Engineering Methodology

## Purpose

Support continuous product discovery and reliable software delivery without
silently changing an approved implementation baseline. This methodology adds
product-specific behavior to the [General Guide](../../protocol/general-guide.md).

Version: `0.2.0` (experimental).

The package manifest is [`method.yaml`](method.yaml). Portable contracts under
[`document-types/`](document-types/) define each type's location, metadata,
ownership, lifecycle, sections, relationships, retrieval, writes, and migration.
This guide owns behavior that spans those types.

## Applicability

Use for maintained products, software projects, reusable agents, developer
tools, and engineering platforms. Do not use it automatically for general
research, incidents, meetings, operations, or personal reflection.

## Artifact Set

- **Project Hub**: required navigation and compact project status.
- **Product Specification**: required when durable product intent exists.
- **Technical Specification**: required before implementation.
- **Discovery Record**: optional exploration, hypotheses, and open questions.
- **Decision Record**: optional, one material decision and its rationale.
- **Change Log**: required when the first delivery baseline is approved.
- **Delivery Baseline**: required for review and build handoff.
- **Implementation Report**: required after implementation.
- **Validation Report**: required before claiming validation.
- **Reconciliation Report**: required when intent/status and repository evidence
  may have drifted.

Do not create empty artifacts for symmetry. Conditional artifacts appear only
when their information and lifecycle justify a separate document.

## Authority

- Product Specification: current approved product intent.
- Technical Specification: current approved intended design.
- Repository source/config/docs: implementation truth.
- Implementation and Validation Reports: attributable evidence snapshots.
- Decision Record and Change Log: accepted historical rationale.
- Discovery Record: unapproved exploration, never delivery scope by default.

## Retrieval Order

1. Query project and artifact metadata.
2. Read the Project Hub.
3. Read Product Specification before Technical Specification.
4. For review/build, read the exact Delivery Baseline references.
5. Inspect repository truth when implementation status matters.
6. Read decisions, discovery, reports, and history only when the task needs
   them.

## Lifecycle

Project states are `IDEA`, `DISCOVERY`, `PLANNED`, `IMPLEMENTING`,
`VALIDATING`, `ACTIVE`, `PARKED`, `BLOCKED`, and `RETIRED`.

Mutable specifications use `DRAFT`, `IN_REVIEW`, `APPROVED`, `SUPERSEDED`, and
`ARCHIVED`. Decision records use `PROPOSED`, `ACCEPTED`, `REJECTED`,
`DEFERRED`, and `SUPERSEDED`. Submitted evidence reports are immutable except
for explicit correction/supersession metadata. Change Logs are append-only.

Delivery baseline states are `CANDIDATE`, `REVIEWED`, `APPROVED_FOR_BUILD`,
`IMPLEMENTED`, `VALIDATED`, `BLOCKED`, `SUPERSEDED`, and `DEVIATED`.

## Discovery And Delivery

Discovery may continue while an approved baseline is implemented. New ideas
remain in Discovery/Future Scope unless explicitly promoted. A material change
creates a new Product/Technical revision and delivery baseline impact review.
Human approval binds to the exact baseline revision after an agent verdict.

## Write Routing

- Product behavior, scope, priorities, or acceptance changes update Product
  Specification and, when material, Decision Record/Change Log.
- Architecture, integration, security, or technical trade-offs update
  Technical Specification and, when material, Decision Record/Change Log.
- Unapproved ideas and unanswered questions update Discovery Record.
- Build agents produce implementation and validation evidence; they do not
  redefine approved requirements.
- Reconciliation uses attributable repository evidence and records `UNKNOWN`
  or drift rather than guessing.

## Relations

Use generic `part_of`, `references`, `supersedes`, and `derived_from` where
their meaning is sufficient. Product-specific relation examples include:

- `product-engineering/baselines`: Delivery Baseline to Product/Technical specs.
- `product-engineering/implements`: Implementation Report to Delivery Baseline.
- `product-engineering/validates`: Validation Report to implementation/baseline.
- `product-engineering/reconciles`: Reconciliation Report to intent and evidence.

## Templates

Templates under [`templates/`](templates/) explain their own fields and
sections. Remove instructional placeholders when creating a real artifact.
The General Guide and this methodology remain authoritative when a template is
incomplete or stale.

## Migration

Use [`migration/README.md`](migration/README.md) for an explicit reviewed
migration. Selecting this method never migrates existing documents by itself.
