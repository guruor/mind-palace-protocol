# OpenCode Client Adapter

## Recommended Mechanism

Use the portable Agent Skill at
`bindings/clients/agent-skill/mind-palace/SKILL.md`. Install it through an
existing configured `skills.paths` directory or as a linked skill under a
supported global/project skill directory. Do not copy protocol behavior into
the skill; it is a thin common-memory bootstrap.

For always-on activation, add a separate bootstrap file path to the existing
`instructions` array in global or project `opencode.json`. OpenCode combines
these instruction files with `AGENTS.md`, so this avoids editing or replacing
existing project/global rules. Preserve every existing array entry and add the
Mind Palace path once.

Do not modify `AGENTS.md` by default. Use an additive, delimited block there
only when the user explicitly selects that fallback and no independent config
hook is available.

## Install

1. Run common-memory install/check and resolve its active release identity.
2. Inspect the effective OpenCode config and existing skill/instruction paths.
3. Snapshot only the config file or link that will change.
4. Prefer one of:
   - append the canonical skill parent to `skills.paths` if not already present;
   - link the canonical skill into an existing skill directory;
   - append a standalone bootstrap path to `instructions` for always-on use.
5. Validate `opencode.json` against `https://opencode.ai/config.json` and run
   `opencode debug config`.
6. Restart OpenCode because config-time files are not hot-reloaded.
7. In a new session, verify the skill is discoverable or the instruction source
   is resolved, then run the installation receipt and common-memory probes.

## Upgrade And Removal

Upgrades switch only the managed skill link/path or standalone bootstrap entry
after the candidate release passes. Exact reinstall is a no-op. Removal deletes
only that managed entry/link and restores its snapshot; it never rewrites
unrelated config or instruction files.

## Official References

- [OpenCode rules and external instruction files](https://opencode.ai/docs/rules/)
- [OpenCode configuration merging and `instructions`](https://opencode.ai/docs/config/)
- [OpenCode Agent Skills discovery](https://opencode.ai/docs/skills/)
