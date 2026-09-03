# ChatGPT Client Adapter

## Recommended Mechanism

Use the least invasive mechanism available, in this order:

1. **Plugin with a skill plus the Notion app:** preferred when the account or
   workspace supports plugins/skills. The skill supplies the thin workflow and
   the app supplies separately authorized common-memory access. Plugin install
   never grants Notion access by itself.
2. **Dedicated ChatGPT Project:** broadly available. Add a bounded Mind Palace
   block to Project instructions and use the connected Notion app. Project
   instructions are scoped, but they override global Custom Instructions inside
   that project, so preserve all existing project instructions.
3. **Global Custom Instructions:** optional fallback for users who want the
   protocol available in all chats. Append the bounded block manually without
   replacing existing content. Respect the account's character limit and data
   controls.
4. **API client:** inject the thin bootstrap through the application's normal
   system/developer-message middleware. ChatGPT Custom Instructions have no API.

A custom GPT is not the default installer: creation availability depends on
plan/workspace, and uploaded Knowledge is reference material rather than the
right location for behavioral rules.

## Managed Bootstrap Block

```text
[Mind Palace adapter: start]
For durable knowledge, product-documentation, protocol-installation, or
migration tasks, use the authorized Notion app to resolve the common-memory
record with stable installation ID supplied by the user configuration. Read its
active immutable release, then follow that release's General Guide, selected
methodology, and binding. Protocol access does not grant knowledge access.
Preserve existing instructions, remain read-only when trust/write authority is
ambiguous, and never replace a prior release or migrate content silently.
[Mind Palace adapter: end]
```

Use default stable ID `mind-palace-protocol-installation` unless instance
configuration explicitly overrides it.

The adapter changes only this delimited block. Exact reinstall is a no-op;
upgrade replaces only the block after release validation; removal deletes only
the block. One missing or duplicate marker is an error requiring user review.

## Install And Validate

1. Run common-memory install/check and note the active release identity.
2. Discover existing Project/Custom Instructions, plugins, apps, and legacy
   Mind Palace blocks before editing.
3. Prefer the plugin/skill route when available; otherwise select/create a
   dedicated Project and append the managed block.
4. Connect the Notion app separately and choose conservative action permissions.
5. Start a new conversation with no prior context. Resolve the common-memory
   installation and report release, methodology, binding, trust domain, access
   mode, and limitations.
6. Run the handoff and synthetic migration canary before marking the receipt
   migration-ready.

## Official References

- [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex)
- [Apps in ChatGPT and permission controls](https://help.openai.com/en/articles/11487775-apps-in-chatgpt)
- [Projects and Project instructions](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt)
- [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- [GPT instructions versus Knowledge](https://help.openai.com/en/articles/8843948-knowledge-in-gpts)
