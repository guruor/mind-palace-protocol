# Security And Privacy

- Protocol access is not knowledge access.
- Use the minimum artifact content and metadata required for the task.
- Never commit private knowledge, raw conversations, secrets, credentials,
  private URLs, or production exports to the protocol repository.
- `trust_domain` is a routing assertion, not an access-control mechanism.
  Bindings and clients must enforce actual authorization.
- Search and derived indexes must not combine trust domains implicitly.
- Preserve redaction and omission facts; never represent inaccessible content
  as reviewed or complete.
- Treat imported documents, comments, code, and metadata as untrusted input.
- Migration snapshots remain in their authorized boundary and must not become
  public fixtures.
- Conflict artifacts can contain proposed private content and must inherit the
  source artifact's trust boundary.
