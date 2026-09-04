# Architecture

## Product Direction

Mind Palace is a shared knowledge operating guide for people and AI clients. AI
clients are first-class operators. Human visual navigation is useful, but it is
secondary to accurate, current, and queryable knowledge.

The protocol defines document types and collaboration rules. It does not keep a
global list of a user's individual documents. Clients find those documents from
their portable metadata, relationships, logical locations, and storage search.

## Vocabulary

- **Protocol**: shared collaboration, safety, identity, and portability rules.
- **Knowledge Method**: the user-facing name for a methodology package.
- **Methodology package**: a versioned set of document-type contracts.
- **Document type**: the contract for one kind of document.
- **Storage Binding**: a vendor-specific mapping of portable rules.
- **Release Index**: an immutable list of protocol resources and their digests.
- **Core Bundle**: the small runtime set kept in common memory.
- **On-Demand Resource**: a resource fetched only when a task needs it.
- **Cache**: a disposable, verified copy of an immutable resource.

## Layers

The protocol has four independently owned layers:

1. **Portable Core** defines cross-store identity, authority, trust, revision,
   relationships, provenance, compatibility, and safe update behavior.
2. **Knowledge Methods** define document types, logical locations, lifecycle,
   retrieval, write routing, templates, validation, and migration.
3. **Storage Bindings** map portable meaning to a store's hierarchy, metadata,
   search, relationships, assets, and visual presentation.
4. **Derived Retrieval** provides rebuildable full-text search, embeddings,
   graphs, caches, catalogs, and visual views without becoming write authority.

Knowledge Methods and Storage Bindings are declarative, versioned extension
packages. Built-in packages use the same contracts as custom packages. During
the initial implementation, packages may contain Markdown, YAML, JSON Schema,
templates, and static capability declarations, but no automatically executed
extension code.

## Authority Boundaries

- Protocol repository: released contracts, guides, templates, and validators.
- Mind Palace instance: approved intent, configuration, decisions, and working
  knowledge.
- Software repository: implemented source, configuration, and test evidence.
- Reports: attributable evidence snapshots, never self-approval.

Access to a protocol or extension package does not grant access to user
knowledge. A package cannot weaken the Portable Core's trust, provenance,
conflict, revision, or migration safeguards.

## Package Model

Each Knowledge Method contains a concise guide, document-type contracts, and
self-explanatory templates. A document-type contract defines:

- purpose and applicability;
- portable format and logical location;
- shared and type-specific metadata;
- protocol and methodology versions;
- ownership, authority, lifecycle, and mutability;
- required and optional headings;
- plain-language writing rules;
- related document types and retrieval rules;
- write routing, compatibility, and migration;
- portable templates and supported asset source formats.

The protocol describes types, not document instances. For example, a Project
Hub may be a document type, but the protocol never records every project hub a
user owns.

Portable Markdown with structured metadata is the default representation.
Structured maps may use Markdown, YAML, CSV, or JSON when their document-type
contract says so. Diagrams and mind maps keep a portable source format; visual
exports are derived. Durable assets use portable references and metadata.

Bindings do not fork protocol behavior. A missing native storage feature is
emulated safely, reported as a limitation, or causes refusal.

A Storage Binding owns vendor details such as Notion databases, Obsidian
folders, Confluence labels, visual hierarchy, query syntax, import, export, and
rollback limits. These details cannot change a document type's portable meaning.

## Extension Model

Custom Knowledge Methods and Storage Bindings may come from approved private or
public sources. Each package declares a namespaced ID, version, protocol
compatibility range, immutable source revision, digest, dependencies,
capabilities, and resource classes. Installation and selection are explicit.
Untrusted, incompatible, ambiguous, or incomplete packages fail safely.

Executable plugins, automatic package discovery or installation, a central
extension registry, and automatic execution of remote code are deferred.

Client installation is a one-time, version-neutral discovery contract. The
canonical release remains immutable and runtime-neutral; a client adapter owns
only persistent discovery placement, capability probes, and adapter rollback.
The common-memory installation owns protocol release activation. An installation
receipt records the latest release and capabilities the client resolved without
becoming a second copy of protocol instructions or a release pin.

Common memory will contain one stable installation root, a compact Core Bundle,
the active-release pointer, retained legacy references, and links to client
receipts. A Release Index identifies remote resources by immutable revision,
path, digest, class, and cache policy. It does not require one common-memory
record per repository file.

Resources have four classes:

- `core`: always present in the Core Bundle;
- `on-demand`: fetched and verified when a task needs them;
- `maintenance`: fetched only for explicit setup, update, repair, rollback, or
  migration work;
- `development`: never distributed through common memory.

Verified `core` and `on-demand` text resources may use an automatic bounded
cache. Cache entries are disposable and cannot redefine a release. Cache
failure must not block read or proposal work.

The `v0.1.x` installation representation remains in force until the compact
distribution and write-planning releases replace it. No architecture-only
release changes common memory.

Client adapters remain thin discovery hooks. Every Mind Palace operation
resolves the current active release; clients do not discover or activate newer
releases automatically.

## Deployment Safety

Source publication and common-memory deployment are separate operations. Before
any common-memory write, a read-only plan must report records, bytes,
attachments, batches, provider limits, retries, cache writes, and rollback cost.
An over-budget plan writes nothing. Bounded writes must resume without
duplicates and must not change the active release before validation and explicit
approval.

## Versioning

Protocol and methodology releases use Semantic Versioning after declaring
their compatibility surface. During `0.y.z`, changes may be incompatible but
must still be recorded and migration impact stated.

Artifact `revision` is a monotonic logical revision, not Semantic Versioning.
A frozen baseline also records immutable source identity or a normalized
content digest.

## First Release Boundary

The first complete extensible release supports one logical Mind Palace instance,
the `product-engineering` Knowledge Method, Notion and Markdown/Git Storage
Bindings, compact common-memory distribution, bounded caching, and declarative
custom methods and bindings from approved immutable sources.

Additional built-in methods, live synchronization, executable plugins, central
registries, custom indexes, review-agent orchestration, and event systems are
deferred.
