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

## Release

1. Update `protocol/manifest.yaml` and document compatibility, changes, and
   rollback in `docs/releases/v<version>.md`.
2. Run `uv run --frozen scripts/validate.py` and
   `uv run --frozen scripts/validate_release.py v<version>`.
3. Merge the validated release commit to `main`.
4. Create an annotated `v<version>` tag at that commit and push the tag.
5. Let `.github/workflows/release.yml` verify tag/version equality, annotated
   tag type, `main` ancestry, and the full protocol suite before publishing the
   GitHub Release.

Do not create the GitHub Release manually or move an existing release tag. The
tag selects the candidate; the workflow validates and publishes it.
