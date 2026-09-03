# Hosted Chat Client Adapter

## Applicability

Use this adapter for a hosted chat client that has:

- persistent account or project custom instructions;
- an authorized connector to the configured common-memory store; and
- enough connector capability to resolve records by stable ID.

Custom instructions are the default hosted-chat mechanism. Skills and plugins
are not required. A host-specific adapter may identify the exact instruction and
connector surfaces, but it must reference this block rather than copy it.

## Managed Custom Instructions

Append this block without replacing existing instructions:

```text
[Mind Palace adapter: start]
When a task installs Mind Palace or uses an authorized knowledge connector for
durable knowledge, first determine whether it targets the configured Mind
Palace scope. For Mind Palace work, resolve the common-memory installation by
exact stable ID mind-palace-protocol-installation, read its active immutable
release, and follow that release's General Guide, selected methodology, and
storage binding before acting.

Protocol access does not grant knowledge access or write authority. Preserve
existing instructions and legacy guidance, remain read-only when scope, trust,
source freshness, or write authority is ambiguous, and never migrate or replace
content silently. Do not apply Mind Palace structure to unrelated connector
work outside the configured scope.
[Mind Palace adapter: end]
```

The adapter changes only this delimited block. Exact reinstall is a no-op;
upgrade replaces only the block after release validation; removal deletes only
the block. Missing or duplicate markers require user review.

## Host Setup

1. Connect and authorize the common-memory service through the host's normal
   connector settings. Do not place credentials in custom instructions.
2. Append the managed block to the host's persistent custom instructions.
3. If project instructions override account instructions, append the same block
   to the project instead of assuming the account block remains effective.
4. Preserve every unrelated instruction and use the narrowest scope that meets
   the user's intent.
5. Start a new conversation after the change; the installation conversation is
   not evidence that persistent activation works.

If the client cannot edit its own host settings, it must print the exact block,
name the settings location, ask the user to append it, and stop. It must not
claim setup passed merely because it used the protocol in the current
conversation.

## Fresh-Client Setup Check

Run this in a new conversation with no copied protocol text or prior chat state:

```text
Run the Mind Palace fresh-client setup check. Resolve the installation using
only your persistent instructions and authorized connector. Report the active
release identity, methodology, binding, trust domain, access mode, and known
limitations. Run only synthetic read, proposal, and stale-source refusal checks;
do not migrate production knowledge. Update the existing client receipt rather
than creating a duplicate.
```

Setup passes when the new conversation independently resolves the active
release and the supported read, proposal, and stale-source refusal checks pass.
The cross-client handoff check remains separate and may stay `not-run`.

## Limits

A hosted chat without persistent instructions is session-only. A hosted chat
without an authorized connector can explain setup but cannot validate common
memory. Neither condition supports durable installation or migration readiness.
