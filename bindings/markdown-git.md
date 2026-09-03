# Markdown And Git Binding

## Representation

One artifact is one UTF-8 `.md` file:

- YAML front matter contains core and methodology metadata;
- the body uses the protocol's documented GFM-compatible subset;
- related assets use portable relative links;
- paths are locators, not stable identities.

Git commit/object identity supplies immutable source provenance. Artifact
revision remains the logical workflow revision.

## Supported Body Baseline

The initial subset includes headings, paragraphs, ordered/unordered/task lists,
block quotes, fenced code, tables, links, images, emphasis, strikethrough, and
inline code. Exact normalization is deferred to the digest proof.

Vendor-specific embeds, permissions, database views, comments, and expiring
asset URLs are not GFM body content. Promote material comments to durable
artifacts and export assets before claiming portability.

## Update And Conflict

Read the current file and Git source version before modification. A proposal
records its base revision and source version/digest. On mismatch, do not write
the canonical file; create a non-canonical conflict artifact in an
instance-configured location outside normal discovery until reconciled.

## Validation

Validate YAML metadata against the selected JSON Schema, local links where
possible, and required methodology sections. Schema success does not establish
factual correctness, authority, or implementation status.
