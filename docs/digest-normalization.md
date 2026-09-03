# Digest Normalization

A frozen baseline uses a logical artifact revision plus an immutable source
version or a `sha256:` content digest. The digest proves the portable artifact
state; it is not a replacement for storage provenance.

## Canonical Input

1. Parse YAML front matter into JSON-compatible data.
2. Remove adapter-derived `content_digest`, `source_version`, and `updated_at`
   fields recursively to avoid self-reference and storage-only churn.
3. Serialize metadata as UTF-8 JSON with sorted keys and compact separators.
4. Normalize body line endings to LF, remove leading/trailing empty lines, and
   include exactly one final newline.
5. Hash `metadata + "\n---\n" + body` with SHA-256.

Do not trim non-empty line whitespace, collapse internal blank lines, reorder
lists/tables, or rewrite Markdown because those changes can alter meaning or
rendering. This deliberately favors a safe false invalidation over treating a
meaningful change as unchanged.

## Consequences

- YAML key ordering and formatting do not affect the digest.
- CRLF versus LF and extra outer blank lines do not affect the digest.
- Body, relation, authority, trust, revision, or meaningful metadata changes
  affect the digest.
- A storage locator change affects the digest because provenance changed.
- Adapter timestamps/source versions and the stored digest do not affect it.

Run `uv run --frozen scripts/digest.py <artifact.md>` to calculate a digest.
