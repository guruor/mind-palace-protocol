# Contributing

1. Classify the change as core, methodology, binding, example, validation, or
   documentation before editing.
2. Keep universal behavior in the General Guide or core schema. Keep domain
   behavior in one methodology. Keep vendor mechanics in one binding.
3. Do not add a core field merely because one methodology needs it.
4. Keep templates self-explanatory, but reference rather than copy generic
   behavior.
5. Preserve unknown extensions and existing compatible consumers.
6. Add valid and invalid fixtures for schema changes.
7. Update compatibility and migration guidance for breaking changes.
8. Run `uv run --frozen scripts/validate.py`.
9. Review the diff for private data, vendor leakage into the core, duplicated
   guidance, and broadened scope.

Structural changes, new methodologies/bindings, and migrations require an
approved decision. Routine corrections and compatible clarifications do not.
