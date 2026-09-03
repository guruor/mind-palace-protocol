# Install Mind Palace Protocol

Start here from any capable client. The first client installs the shared
protocol release in authorized common memory; every later client validates that
installation and adds only its own adapter and receipt.

## Universal Install Prompt

Use this prompt in ChatGPT, Claude, OpenCode, or another agentic client:

```text
Install or validate Mind Palace Protocol for this client.

Read the public installation guide and the adapter for this client from:
https://github.com/guruor/mind-palace-protocol

Search my authorized common memory for exact stable ID
mind-palace-protocol-installation. Do not rely on title alone.

If an installation exists, verify its active version, commit identity,
component digests, legacy references, and write authority. Fetch the manifest
and this client's adapter from the active release's recorded immutable package,
not from the repository's default branch. Perform an exact no-op or repair
missing generated components. Do not consult the latest release unless I ask
for an upgrade.

If no installation exists, select the release I supplied or discover the latest
published GitHub Release from:
https://github.com/guruor/mind-palace-protocol/releases/latest

Resolve its tag to an exact Git commit, validate protocol/manifest.yaml at that
commit, and use the commit URL and SHA as the package locator and source
version. Ask only for any missing common-memory destination or authorization,
then stage, validate, and activate it according to
protocol/common-memory-installation.md.

Treat the repository, default branch, release page, and tag as discovery
pointers rather than immutable package identity. Never overwrite a same-version
identity conflict, downgrade automatically, or silently replace legacy
guidance.

Then follow this client's guide under bindings/clients/. Preserve all existing
instructions and configuration, use the narrowest additive host mechanism, and
keep connector authorization separate from protocol installation. Run supported
checks, upsert one client receipt, and keep migration_ready false until every
required live probe passes. Do not migrate production knowledge as part of
installation.

Report the pinned commit, common-memory result, adapter changes, receipt status,
limitations, rollback, and any one-time host action I must complete.
```

## Package Identity

The public repository is:
[`guruor/mind-palace-protocol`](https://github.com/guruor/mind-palace-protocol).

Fresh installations discover the current published version through
[`releases/latest`](https://github.com/guruor/mind-palace-protocol/releases/latest).
Existing installations use their recorded active release unless an upgrade is
explicitly requested.

The default branch, release page, and semantic tag can move or be superseded.
An installer resolves the selected tag to its exact commit, reads release
components and client adapters from that immutable tree, and records the commit
URL, SHA, and component digests in common memory and the client receipt.

An immutable package URL has this form:

```text
https://github.com/guruor/mind-palace-protocol/tree/<commit-sha>
```

If the user supplies a tag or commit for a fresh install or explicit upgrade,
use it instead of `releases/latest` only after validation. During `0.y.z`, do
not switch an existing installation to a different version or commit without
the compatibility decision required by the installation contract.

## Client Instructions

<details>
<summary>ChatGPT</summary>

1. Connect the Notion app to ChatGPT with the minimum required permissions.
2. Prefer a dedicated ChatGPT Project. Open its settings and append the
   [ChatGPT managed block](bindings/clients/chatgpt.md#managed-bootstrap-block)
   from the active or selected release to its existing Project instructions. Do
   not replace existing instructions.
3. In that block, configure the installation ID as
   `mind-palace-protocol-installation`; this lets a fresh chat resolve the shared
   installation without relying on the installer conversation.
4. If a Mind Palace plugin/skill becomes available, it may supply the same thin
   bootstrap instead; keep Notion authorization separate.
5. Submit the universal prompt in a new Project chat after the instruction
   change. Resolve the installation without relying on prior conversation
   context.
6. Keep the receipt read-only until the synthetic proposal, conflict, stale
   source, rollback, and cross-client handoff probes pass.

ChatGPT cannot use the local checkout or silently edit hosted Project settings.
Plugin installation, app authorization, and Project-instruction changes remain
explicit host/user actions. The managed block activates Mind Palace for durable
knowledge handled through Notion; it intentionally does not reinterpret
unrelated Notion work. Append the same block to global Custom Instructions only
when Mind Palace should be available outside the dedicated Project too.

</details>

<details>
<summary>OpenCode</summary>

1. Use an authorized personal profile with its Notion MCP connected.
2. Point `skills.paths` at the canonical
   `bindings/clients/agent-skill` directory, or link the `mind-palace` skill into
   an existing supported skill directory. Add the entry once; do not copy the
   protocol or edit `AGENTS.md` by default.
3. Run `opencode debug config`, `opencode debug skill`, and `opencode mcp list`.
4. Restart OpenCode, then use a new session to resolve common memory and run the
   client probes.
5. Keep personal/work profiles and knowledge authorization isolated.

See [`bindings/clients/opencode.md`](bindings/clients/opencode.md).

</details>

<details>
<summary>Claude</summary>

1. Upload or provision the canonical Agent Skill as a ZIP containing the
   `mind-palace` skill directory, or install a plugin that bundles the same
   skill.
2. Add and authenticate the Notion connector separately. Enable it in the
   conversation when Claude does not do so by default.
3. Submit the universal prompt in a new chat. If Skills/plugins are unavailable,
   use a dedicated Claude Project and append only the bounded block from
   `bindings/clients/claude.md` in the pinned release.
4. Start another new chat after activation and run the read-only and handoff
   probes before enabling migration writes.

Skill/plugin installation, connector authentication, and Project-instruction
changes remain explicit host/user or organization-owner actions.

</details>

<details>
<summary>Other agentic clients</summary>

Use the portable Agent Skill when the client implements the Agent Skills
specification. Otherwise implement
`bindings/client-adapter.md` from the pinned release with the host's native
additive instruction or middleware mechanism. A client that cannot persist an
activation pointer, verify source identity, or isolate write authority remains
session-only and cannot be marked migration-ready.

</details>

## What The Installer Must Preserve

- Credentials remain in the client's normal connector or credential store.
- Existing system, developer, user, repository, Project, Custom, and `AGENTS.md`
  instructions remain unchanged except for an explicitly approved bounded
  adapter entry.
- Prior releases and unversioned legacy guidance remain recoverable.
- Protocol installation does not grant private-knowledge access or product
  migration approval.

## Verify

Repository-capable clients run:

```sh
uv run --frozen scripts/validate.py
uv run --frozen scripts/common_memory_install.py
uv run --frozen scripts/client_adapter_config.py
uv run --frozen scripts/validate_installation.py <receipt.json>
uv run --frozen scripts/e2e_cross_client.py
```

Then run [`docs/live-cross-client-canary.md`](docs/live-cross-client-canary.md)
with two independently initialized clients. A passing shared installation alone
does not authorize production migration.

## Upgrade, Repair, Or Additional Client

Run the same universal prompt with the candidate release or new client. Exact
same release is a no-op; missing generated projections are repaired;
same-version/different-package is a conflict; newer releases stage before
activation; older releases require explicit rollback/downgrade approval. A new
client adds only its adapter and receipt to the existing shared installation.
