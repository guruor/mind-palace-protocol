# Extension Authoring

Mind Palace supports two declarative extension types: Knowledge Methods and
Storage Bindings. Built-in and external packages use the same contracts.

## Shared Package Identity

Every package declares:

- a namespaced ID such as `team/research-method`;
- package type and Semantic Version;
- compatible protocol versions;
- source identity;
- resource paths, classes, cache policy, and purpose;
- dependencies and provided capabilities.

Packages contain no private user documents. Access to a package does not grant
access to a Mind Palace instance.

A built-in package declares its path inside the immutable protocol release. The
outer release supplies its revision and integrity. A remote package declares its
locator and revision; the separately approved extension-source reference carries
the expected manifest digest. This avoids placing a manifest's own digest inside
the content being hashed.

## Knowledge Method

A Knowledge Method defines document types for one kind of work. Its package
manifest validates against `schemas/knowledge-method.schema.json`.

Each document type validates against `schemas/document-type.schema.json` and
defines:

1. purpose and when to use it;
2. portable format and logical location;
3. shared and type-specific metadata;
4. ownership, authority, lifecycle, and mutability;
5. required and optional sections;
6. plain-language style and audience;
7. related types and how to query them;
8. retrieval and write-routing rules;
9. compatibility and migration guidance;
10. a portable template.

A method extends the Portable Core. It cannot remove identity, provenance,
trust, revision, relationship, conflict, or migration safeguards.

## Storage Binding

A Storage Binding maps portable meaning to one store. Its package manifest
validates against `schemas/storage-binding.schema.json`.

The binding declares storage capabilities and limitations. It explains how to
map logical locations, metadata, relationships, search, visual views, assets,
export, import, and rollback. It must report unsupported behavior instead of
silently losing information.

## Instance Selection

An instance configuration selects a Knowledge Method by work mode and a primary
Storage Binding. It validates against `schemas/instance-config.schema.json`.
The configuration references packages by namespaced ID and version; it does not
copy their rules.

## External Source Approval

Before first use, add an approved extension-source reference to instance
configuration. The reference records package ID, type, version, immutable HTTPS
manifest locator, exact source revision, expected manifest digest, and an
approval reference.

Resolution follows this order:

1. fetch no more than 200 KiB from the approved HTTPS locator;
2. reject redirects, local hosts, and private network addresses;
3. verify the exact manifest digest;
4. verify ID, type, version, and source revision against the approval;
5. validate the declarative package schema;
6. check protocol compatibility and dependencies;
7. reject duplicate document-type ownership;
8. check required binding capabilities;
9. admit eligible immutable text resources to the normal bounded cache.

If any check fails, do not select the package. Keep the current valid method or
binding and remain read-only when the requested work cannot be represented
safely.

## Resource Classes

- `core`: always part of the small runtime bundle.
- `on-demand`: fetched only when a task needs it.
- `maintenance`: fetched for explicit setup or maintenance work.
- `development`: never distributed through common memory.

Use `always` cache policy only with `core`. Use `automatic` for small immutable
text resources that improve normal work. Use `never` for maintenance,
development, binary, or sensitive resources.

## Safety Limit

Packages are data, not executable plugins. Do not automatically run code from a
package. Package selection is explicit. Automatic package discovery, arbitrary
dependency installation, executable hooks, and a central registry remain
deferred.
