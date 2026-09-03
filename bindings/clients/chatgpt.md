# ChatGPT Client Adapter

## Recommended Mechanism

Use ChatGPT Custom Instructions as the default adapter for normal chats. Append
the canonical block from
[`hosted-chat.md`](hosted-chat.md#managed-custom-instructions) without replacing
existing instructions.

For a dedicated ChatGPT Project, use Project instructions when project-specific
scope is preferable or when Project instructions override account Custom
Instructions. An API client injects the same thin bootstrap through its normal
system/developer-message middleware. A custom GPT, plugin, Skill, or uploaded
Knowledge file is not required for installation.

## Install

1. Resolve the active or selected immutable protocol release.
2. Connect the Notion app separately with the minimum required permissions.
3. Open Custom Instructions and append the canonical hosted-chat managed block.
4. If the intended Project overrides account instructions, append the block to
   that Project's existing instructions instead.
5. Start a new conversation and run the fresh-client setup check from
   [`hosted-chat.md`](hosted-chat.md#fresh-client-setup-check).
6. Update one ChatGPT receipt with the observed checks. `handoff_probe` may
   remain `not-run`; do not claim cross-client readiness until the separate
   handoff check passes.

ChatGPT cannot silently modify account or Project instructions. When asked to
install, it must provide the exact block and settings location, then wait for the
user to confirm the change before requesting a fresh conversation.

## Protocol Updates And Removal

Protocol updates require no Custom Instructions change: each Mind Palace task
resolves the active common-memory release. Replace the delimited block only for
an explicitly approved change to the discovery contract. Removal deletes only
that block; Notion authorization is revoked separately through ChatGPT settings.

## Official References

- [Apps in ChatGPT and permission controls](https://help.openai.com/en/articles/11487775-apps-in-chatgpt)
- [Projects and Project instructions](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)
- [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- [GPT instructions versus Knowledge](https://help.openai.com/en/articles/8843948-knowledge-in-gpts)
