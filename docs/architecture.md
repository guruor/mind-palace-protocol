# Architecture

## Layers

The protocol has four independently owned layers:

1. **Portable core** defines cross-store identity, authority, trust, revision,
   relationships, provenance, and compatibility.
2. **Methodology packages** define domain artifacts, lifecycle, retrieval,
   write routing, templates, validation, and migration.
3. **Bindings** map portable semantics to storage/client capabilities and
   report limitations.
4. **Derived discovery** provides rebuildable catalogs, full-text search,
   embeddings, graphs, or caches without becoming write authority.

## Authority Boundaries

- Protocol repository: released contracts, guides, templates, and validators.
- Mind Palace instance: approved intent, configuration, decisions, and working
  knowledge.
- Software repository: implemented source, configuration, and test evidence.
- Reports: attributable evidence snapshots, never self-approval.

## Package Model

Each methodology contains a concise guide plus self-explanatory templates.
Templates explain their own fields and sections. The guide owns behavior that
spans artifacts: applicability, lifecycle, relationships, retrieval order,
write routing, compatibility, validation, and migration.

Bindings do not fork protocol behavior. A missing native storage feature is
emulated safely, reported as a limitation, or causes refusal.

Client installation is a protocol-level staged activation contract. The
canonical release remains immutable and runtime-neutral; a client adapter owns
placement, activation pointers, capability probes, and rollback mechanics. An
installation receipt records what was resolved and tested without becoming a
second copy of protocol instructions.

Common memory contains one stable installation root, generated immutable
release projections, the active-release pointer, retained legacy references,
and links to client receipts. Client adapters are thin discovery hooks. This
allows one shared release installation and independent non-destructive client
activation without making any client's instruction file canonical.

## Versioning

Protocol and methodology releases use Semantic Versioning after declaring
their compatibility surface. During `0.y.z`, changes may be incompatible but
must still be recorded and migration impact stated.

Artifact `revision` is a monotonic logical revision, not Semantic Versioning.
A frozen baseline also records immutable source identity or a normalized
content digest.

## First Release Boundary

V1 supports one logical Mind Palace instance, the Notion binding, the
Markdown/Git portable representation, and `product-engineering`. Additional
instances, methodologies, live synchronization, custom indexes, review-agent
orchestration, and event systems are deferred.
