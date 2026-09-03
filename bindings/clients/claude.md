# Claude Client Adapter

## Recommended Mechanism

Use Claude's persistent personalization or Project instructions as the default
adapter for hosted Claude chats. Append the canonical block from
[`hosted-chat.md`](hosted-chat.md#managed-custom-instructions) without replacing
existing instructions. Use a dedicated Project when the protocol should have
project scope rather than account scope.

Claude Code and API clients are agentic clients rather than hosted-chat-only
clients. They may use the portable Agent Skill or inject the thin bootstrap
through their supported instruction mechanism, but hosted Claude does not
require a Skill or plugin for Mind Palace setup.

## Install

1. Resolve the active or selected immutable protocol release.
2. Add and authenticate the Notion connector separately with the minimum
   required permissions. Enable it in the conversation when the host requires
   that action.
3. Append the canonical hosted-chat managed block to the selected persistent
   personalization or Project instruction surface.
4. Start a new conversation and run the fresh-client setup check from
   [`hosted-chat.md`](hosted-chat.md#fresh-client-setup-check).
5. Update one Claude receipt with the observed checks. `handoff_probe` may
   remain `not-run`; do not claim cross-client readiness until the separate
   handoff check passes.

Hosted Claude cannot silently modify personalization, Project instructions, or
connector authorization. When asked to install, it must provide the exact block
and settings location, then wait for the user to confirm the change before
requesting a fresh conversation.

## Protocol Updates And Removal

Protocol updates require no personalization or Project-instruction change: each
Mind Palace task resolves the active common-memory release. Replace the
delimited block only for an explicitly approved change to the discovery
contract. Removal deletes only that block; connector authorization is revoked
separately through Claude settings.

## Official References

- [Configure remote MCP connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Claude personalization and Project instructions](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)
