# Install Mind Palace Protocol

## What The User Does

Give a capable agent access to an immutable protocol release and say:

> Install Mind Palace protocol in my authorized common memory, then set up this
> client without replacing any existing instructions. Validate the installation
> and report anything that needs my approval.

For the first installation, identify the intended Notion/configuration parent if
it is not already configured. Credentials stay in the client's normal Notion
connection and are never copied into the protocol or installation record.

## What The Agent Does

1. Validate the immutable package and read `protocol/manifest.yaml`.
2. Search common memory for stable ID `mind-palace-protocol-installation` and
   inspect legacy protocol/bootstrap guidance.
3. Install, no-op, repair, or stage the release according to
   `protocol/common-memory-installation.md`.
4. Preserve prior releases and legacy guidance. Ask before incompatible upgrade,
   downgrade, behavior migration, or retiring old write authority.
5. Select the current host adapter and add only its managed reference/block.
6. Preserve all existing system, developer, user, repository, Project, Custom,
   and `AGENTS.md` instructions.
7. Restart/reopen the client when its adapter requires it and run installation
   probes in a fresh session.
8. Upsert one client receipt and report `read`, `propose`, or `update` readiness.

## Additional Clients

For each additional client, use the same request. The shared installation phase
should return `no-op` or `repaired`; only the new client adapter and receipt are
added.

### OpenCode

Preferred: install the bundled Agent Skill additively through `skills.paths` or
a supported skill directory. Use a separate `instructions` entry only when
always-on activation is required. Do not edit `AGENTS.md` by default. Validate
resolved configuration, restart OpenCode, and test from a new session. See
[`bindings/clients/opencode.md`](bindings/clients/opencode.md).

### ChatGPT

Preferred when available: install a plugin containing the Mind Palace skill and
connect its Notion app separately. Otherwise use a dedicated ChatGPT Project and
append the managed block to existing Project instructions. Global Custom
Instructions are an optional manual fallback. See
[`bindings/clients/chatgpt.md`](bindings/clients/chatgpt.md).

### Claude

Preferred: upload or provision the bundled Agent Skill; a Claude plugin may
bundle the same skill with connector configuration. Connect and authenticate
the Notion connector separately, and enable it in the conversation when
required. Otherwise append the managed block to a dedicated Claude Project's
existing instructions. See
[`bindings/clients/claude.md`](bindings/clients/claude.md).

### Other Clients

Use the portable Agent Skill when supported. Otherwise implement the operations
in [`bindings/client-adapter.md`](bindings/client-adapter.md) using the host's
native additive instruction/middleware mechanism. A client without persistent
activation or source-identity verification remains session-only and cannot be
marked migration-ready.

## Verify

Repository-capable clients run:

```sh
uv run --frozen scripts/validate.py
uv run --frozen scripts/common_memory_install.py
uv run --frozen scripts/client_adapter_config.py
uv run --frozen scripts/validate_installation.py <receipt.json>
uv run --frozen scripts/e2e_cross_client.py
```

Then run the synthetic live canary in
[`docs/live-cross-client-canary.md`](docs/live-cross-client-canary.md). Protocol
installation alone does not authorize product migration.

## Upgrade Or Repair

Run the same installation request with the candidate immutable release. Exact
same release is a no-op; missing generated projections are repaired;
same-version/different-package is a conflict; newer releases stage before
activation; older releases require explicit rollback/downgrade approval. The
agent changes only managed protocol records and adapter entries.
