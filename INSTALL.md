# Install Mind Palace Protocol

This is the only installation entry point a user needs. Shared protocol
installation and updates happen only after an explicit user request. Each client
adds a version-neutral discovery adapter once, then follows whatever release the
common-memory installation marks active.

**In plain terms:** you install Mind Palace once into shared memory, then give
each AI client a small one-time "adapter" (a short instruction or Skill). After
that, whenever a client does Mind Palace work it reads the currently active
release on its own — so a protocol update never requires reinstalling clients or
re-editing their instructions.

## One-Link Prompt

Give a client this prompt:

```text
Install or validate Mind Palace Protocol by following:
https://github.com/guruor/mind-palace-protocol/blob/main/INSTALL.md

Follow the guide for your actual host capabilities. If a host setting or
connector requires my action, give me the exact text and location, then stop and
wait for confirmation. Do not claim persistent setup from this conversation
alone and do not migrate production knowledge during installation.
```

## Explicit Common-Memory Operations

Use an explicit request for every shared protocol lifecycle change:

- `Install Mind Palace protocol from <release>.`
- `Update Mind Palace protocol to <release>.`
- `Repair the active Mind Palace protocol installation.`
- `Roll back Mind Palace protocol to <retained-release>.`

`Validate the active Mind Palace protocol installation` is read-only. Ordinary
Mind Palace and Notion work resolves the active release and must not imply any of
these lifecycle operations.

## Instructions For The Installing Client

Complete these steps in order:

1. Identify the current host as a hosted chat, an agentic client, or a
   session-only client.
2. Check whether the host can read the public repository, access authorized
   common memory, and persist an additive adapter without replacing existing
   instructions.
3. Resolve the shared active release. Install or update it only when the user's
   request explicitly asks for that common-memory operation.
4. Follow exactly one client section from this guide.
5. If the host cannot edit its own persistent settings, print the exact custom
   instruction block and the host setting where the user must append it. Stop
   until the user confirms completion.
6. After first-time client setup, require a new conversation or session and run the
   Fresh-Client Setup Check. The installer conversation is not persistence
   evidence.
7. Update one client receipt. Do not create duplicate receipts and do not mark
   migration readiness while required checks remain unrun.

## Resolve Or Install Common Memory

Search authorized common memory for exact stable ID
`mind-palace-protocol-installation`. Do not rely on title alone.

If an installation exists:

- verify its active version, commit identity, Release Index, and required core
  resource digests;
- confirm its legacy references, trust domain, and effective write authority;
- fetch the manifest and adapter from its recorded immutable package, not from
  the repository's default branch;
- perform an exact no-op or repair only missing core resources; and
- do not consult the latest release unless the user asks for an upgrade.

If no installation exists:

- use a user-supplied release or discover the latest published release at
  [`releases/latest`](https://github.com/guruor/mind-palace-protocol/releases/latest);
- resolve the tag to an exact Git commit and validate
  `protocol/manifest.yaml` at that commit;
- use the commit URL and SHA as package identity; and
- ask only for missing destination or authorization, then follow
  [`protocol/common-memory-installation.md`](protocol/common-memory-installation.md).

Repository branches, release pages, and tags are discovery pointers. The exact
commit, Release Index, and core resource digests are installation evidence.
Never overwrite a
same-version identity conflict, downgrade automatically, replace legacy
guidance, or infer private-knowledge authority from protocol access.

## Choose The Client Adapter

<details>
<summary>Hosted chat: any provider</summary>

Use [`bindings/clients/hosted-chat.md`](bindings/clients/hosted-chat.md) for a
hosted chat with persistent custom instructions and an authorized knowledge
connector. This is the canonical binding for ChatGPT, hosted Claude, and other
chat providers with equivalent capabilities.

The normal setup is:

1. The user connects and authorizes Notion or the configured common-memory
   service through the host's connector settings.
2. The client prints the exact managed block from the hosted-chat binding.
3. The user appends it to existing account custom instructions, or to Project
   instructions when project scope is preferred or overrides account settings.
4. The user starts a new conversation and runs the one-time Fresh-Client Setup
   Check.

Skills and plugins are not required. If the host lacks persistent instructions
or an authorized connector, report session-only or documentation-only status
instead of claiming installation.

</details>

<details>
<summary>ChatGPT</summary>

Follow [`bindings/clients/chatgpt.md`](bindings/clients/chatgpt.md).

Use global Custom Instructions when Mind Palace should be available in normal
chats. Use Project instructions when the setup should be scoped to one Project
or that Project overrides account instructions. Connect the Notion app
separately. ChatGPT must provide the exact custom-instruction block because it
cannot silently edit these host settings.

</details>

<details>
<summary>Claude chat</summary>

Follow [`bindings/clients/claude.md`](bindings/clients/claude.md).

Use persistent personalization or Project instructions and connect Notion
separately. A Skill or plugin is not required for hosted Claude. Claude Code is
an agentic client and may use the Agent Skill route instead.

</details>

<details>
<summary>OpenCode</summary>

Follow [`bindings/clients/opencode.md`](bindings/clients/opencode.md).

Use an authorized profile with its Notion MCP connected. Point `skills.paths`
at the canonical `bindings/clients/agent-skill` directory, or link the
`mind-palace` skill into an existing supported skill directory. Add the entry
once; do not copy the protocol or edit `AGENTS.md` by default.

Run `opencode debug config`, `opencode debug skill`, and `opencode mcp list`,
then restart OpenCode and run the one-time Fresh-Client Setup Check in a new
session.
Keep personal/work profiles and knowledge authorization isolated.

</details>

<details>
<summary>Other agentic clients</summary>

Use the portable Agent Skill when the client implements the Agent Skills
specification. Otherwise implement
[`bindings/client-adapter.md`](bindings/client-adapter.md) with the host's native
additive instruction or middleware mechanism. Preserve existing configuration
and ask before any host-level change outside already authorized scope.

</details>

<details>
<summary>Session-only clients</summary>

A client that cannot persist instructions, verify package identity, or isolate
write authority may use the active protocol per session in `read` or `propose`
mode. It must not claim durable installation or migration readiness. Give it the
one-link prompt at the start of each relevant conversation.

</details>

## Validation Stages

Use these names instead of the ambiguous phrase "run the live canary":

1. **Fresh-Client Setup Check:** after one-time client setup, a new
   conversation/session independently
   resolves the active release and runs synthetic read, proposal, and stale-
   source refusal checks. This proves the client adapter is active.
2. **Cross-Client Handoff Check:** Client A emits a schema-valid synthetic
   handoff and a separately initialized Client B consumes it without hidden chat
   history. This proves portability between clients.
3. **Approved Write Canary:** with explicit bounded approval, migrate one
   synthetic artifact, repeat the request to prove idempotency, then execute and
   verify rollback. This tests write behavior, not installation.

Run the stages through
[`docs/live-cross-client-canary.md`](docs/live-cross-client-canary.md). A client
may pass setup while handoff and write checks remain `not-run`. A passing
single-client receipt does not claim cross-client or production-write readiness.

## Repository Validation

Repository-capable clients run:

```sh
uv run --frozen scripts/validate.py
uv run --frozen scripts/common_memory_install.py
uv run --frozen scripts/client_adapter_config.py
uv run --frozen scripts/validate_installation.py <receipt.json>
uv run --frozen scripts/e2e_cross_client.py
```

## Preserve And Roll Back

- Keep credentials in the host's connector or credential store.
- Preserve existing system, developer, user, repository, Project, Custom, and
  `AGENTS.md` instructions.
- Reconstruct prior releases from immutable repository tags when rollback is
  requested; retain only explicitly exempted legacy guidance in common memory.
- Treat protocol installation, connector authorization, private-knowledge
  access, and production migration approval as separate permissions.
- Remove only the managed adapter block/path/link during client rollback.

## Upgrade, Repair, Or Add A Client

Explicitly ask to install, update, repair, roll back, or add a client. Exact same
release is a no-op; missing core resources are repaired;
same-version/different-package is a conflict; newer releases stage before
activation; older releases require explicit rollback/downgrade approval. A
protocol update never edits existing client adapters. A new client adds its
version-neutral adapter and one receipt to the existing shared installation.
