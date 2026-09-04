# Notion Runtime Binding

Use this short binding during normal Mind Palace work. Read the detailed
[`notion.md`](notion.md) only when a task needs uncommon representation, export,
asset, permission, or migration behavior.

## Find

- Query metadata before loading full page bodies.
- Resolve documents by stable ID when available; do not trust title alone.
- Use database properties and relations for fast discovery, but treat them as a
  Notion representation of portable metadata.
- Follow only the relationships needed by the current task.

## Read And Write

- Read the current properties and body before a material update.
- Re-read immediately before writing when stale state would matter.
- Make the smallest complete update and preserve unrelated blocks, properties,
  relations, and unknown metadata.
- Serialize writes per document. Preserve a conflict instead of overwriting a
  changed source.
- Keep protocol access separate from private knowledge authorization.

## Limits

- Notion hierarchy, databases, views, icons, and covers are visual or
  vendor-specific presentation, not portable document meaning.
- Comments, expiring uploads, and unsupported blocks need explicit export or
  migration handling.
- If required metadata, permissions, or relationships cannot be preserved,
  remain read-only and report the gap.
