# Claude Client Adapter

## Recommended Mechanism

Use the least invasive mechanism available, in this order:

1. **Provisioned Agent Skill:** preferred for Team and Enterprise organizations.
   An owner uploads the portable Agent Skill at
   `bindings/clients/agent-skill/mind-palace/` as a ZIP containing the skill
   directory at its root. Claude provisions organization skills enabled by
   default, while each user can still disable them.
2. **Personal Agent Skill:** upload the same ZIP through `Customize > Skills`.
   Installation or enablement is a user-controlled host action; the skill can
   automate common-memory install/check only after it is active.
3. **Claude plugin:** package the same skill with connector configuration when
   paid-plan plugin distribution is appropriate. A plugin can make the workflow
   and connector definition available together, but it does not grant access to
   the connected service.
4. **Dedicated Claude Project:** append the managed bootstrap block below to
   Project instructions when Skills or plugins are unavailable. Preserve all
   existing Project instructions. Account-wide instructions are a last resort.
5. **Claude Code or API client:** install the portable skill through the host's
   supported skill mechanism, or inject the thin bootstrap through the
   application's normal system/developer-message middleware.

## Common-Memory Connection

Use an authorized Notion connector or trusted remote MCP server. Connector
configuration, OAuth, and protocol installation are separate operations:

- on Team and Enterprise, an owner adds a custom connector and each user then
  connects and authenticates it;
- on an individual account, the user adds and authenticates the connector;
- enable the connector in each conversation when the host does not enable it by
  default.

Never place credentials, OAuth secrets, or copied private content in the skill,
plugin, Project instructions, installation record, or handoff. A discoverable
skill without an enabled connector is not a durable installation and cannot be
marked migration-ready.

## Managed Bootstrap Block

```text
[Mind Palace adapter: start]
For durable knowledge, product-documentation, protocol-installation, or
migration tasks, use the authorized Notion connector to resolve the common-
memory record with stable installation ID supplied by the user configuration.
Read its active immutable release, then follow that release's General Guide,
selected methodology, and binding. Protocol access does not grant knowledge
access. Preserve existing instructions, remain read-only when trust/write
authority is ambiguous, and never replace a prior release or migrate content
silently.
[Mind Palace adapter: end]
```

Use default stable ID `mind-palace-protocol-installation` unless instance
configuration explicitly overrides it. The adapter changes only this delimited
block. Exact reinstall is a no-op; upgrade replaces only the block after release
validation; removal deletes only the block. One missing or duplicate marker is
an error requiring user review.

## Install And Validate

1. Run common-memory install/check and note the active release identity.
2. Discover existing Skills, plugins, Project/account instructions, connectors,
   and legacy Mind Palace guidance before changing anything.
3. Prefer a provisioned/personal skill or plugin. Otherwise append the managed
   block to a dedicated Project's existing instructions.
4. Ask the user or organization owner to complete any required upload,
   installation, enablement, and connector authorization in Claude.
5. Start a new conversation with no prior context and explicitly enable the
   connector if required. Resolve the common-memory installation and report
   release, methodology, binding, trust domain, access mode, and limitations.
6. Run the handoff and synthetic migration canary before marking the receipt
   migration-ready.

## Upgrade And Removal

Stage and validate the candidate common-memory release before changing the
managed skill/plugin version or instruction block. Preserve the prior active
release and adapter state for rollback. Removal disables or removes only the
managed skill/plugin/block and connector reference; connector authorization is
revoked separately by the user or administrator.

## Official References

- [Create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Provision organization Skills](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization)
- [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Configure remote MCP connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Claude personalization and Project instructions](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)
