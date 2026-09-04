# Extension Authoring

Mind Palace supports two declarative extension types: Knowledge Methods and
Storage Bindings. This release defines their contracts. A later release will add
resolution from approved external sources.

## Shared Package Identity

Every package declares:

- a namespaced ID such as `team/research-method`;
- package type and Semantic Version;
- compatible protocol versions;
- immutable source locator, revision, and SHA-256 digest;
- resource paths, classes, cache policy, and purpose;
- dependencies and provided capabilities.

Packages contain no private user documents. Access to a package does not grant
access to a Mind Palace instance.

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

## Resource Classes

- `core`: always part of the small runtime bundle.
- `on-demand`: fetched only when a task needs it.
- `maintenance`: fetched for explicit setup or maintenance work.
- `development`: never distributed through common memory.

Use `always` cache policy only with `core`. Use `automatic` for small immutable
text resources that improve normal work. Use `never` for maintenance,
development, binary, or sensitive resources.

## Current Limit

Packages are data, not executable plugins. Do not automatically run code from a
package. External source trust, dependency resolution, and installation are
deferred until the custom-package foundation release.
