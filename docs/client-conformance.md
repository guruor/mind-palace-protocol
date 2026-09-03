# Client Conformance

## Installation Cases

Every client adapter must demonstrate:

1. fresh staged installation and post-activation resolution;
2. same-version no-op/repair without duplicate copies;
3. compatible upgrade with rollback pointer preserved;
4. migration-required upgrade blocked until approval;
5. newer installed version protected from automatic downgrade;
6. unversioned legacy guidance retained until mapped or explicitly retired;
7. invalid installation constrained to read-only behavior;
8. parallel installations with only one write authority per instance;
9. interrupted activation restored or resumed deterministically;
10. uninstall/rollback restoring the prior validated pointer and configuration.

The executable receipt cases are in
`tests/conformance/client-installation-cases.yaml`.

Before those client-local cases, run the shared-installation scenario. It proves
first install, exact no-op, missing-component repair, same-version package
conflict, staged/approved upgrade, downgrade refusal, approved rollback, legacy
preservation, and client-receipt deduplication. The adapter-configuration
scenario proves existing OpenCode configuration and ChatGPT/Claude instruction
text survive install, reinstall, upgrade, and malformed-marker refusal.

```sh
uv run --frozen scripts/common_memory_install.py
uv run --frozen scripts/client_adapter_config.py
```

## Two-Client Handoff Test

Use two independently initialized clients, such as OpenCode and ChatGPT or
Claude. Do not give Client B the originating conversation.

1. Install the same immutable protocol/methodology release in both clients and
   validate both installation receipts.
2. Give each client separately authorized access to the same synthetic instance.
3. Client A resolves a synthetic project, prepares a migration preflight, and
   emits `schemas/client-handoff.schema.json` containing references rather than
   copied private bodies or credentials.
4. Client B runs `uv run --frozen scripts/validate_handoff.py <handoff.json>`,
   independently resolves the protocol and
   instance, fetches artifacts by stable ID, and verifies source identities.
5. Client B reproduces artifact classification, mapping, omissions, conflicts,
   and required approval without hidden context.
6. Change one source artifact after handoff. Client B must refuse that stale
   item and preserve a conflict rather than write.
7. With bounded approval, Client B migrates one synthetic canary; otherwise it
   remains read-only and returns the executable plan.
8. Compare counts, stable IDs, revisions/digests, relations, authority, trust
   boundaries, and omission reports.

The handoff passes only if Client B can continue safely and deterministically.
Equivalent prose is not enough when artifact identity, source freshness,
authorization, or omissions differ.

Run `uv run --frozen scripts/e2e_cross_client.py` for the local simulation. It
uses independent synthetic OpenCode and ChatGPT installation identities and
proves fresh handoff, idempotent migration, stale-source refusal, conflict
preservation, trust isolation, refreshed migration, and rollback. This test does
not substitute for the fresh-client and cross-client checks below.

## Product Migration Readiness

After installation conformance, each product still needs a product-specific
preflight. A passing installation proves client capability; it does not prove
that a particular corpus is safe to migrate.
