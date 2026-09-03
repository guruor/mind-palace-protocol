# Client Adapter Contract

A client adapter maps the runtime-neutral installation contract to one host. It
must reference an immutable protocol package; it must not maintain a forked copy
of the General Guide, schemas, or methodology rules.

## Required Operations

- `discover`: enumerate active/staged protocol pointers, receipts, copied legacy
  guidance, adapter configuration, and effective write authority;
- `stage`: make a candidate immutable release resolvable without activating it;
- `resolve`: load the manifest, General Guide, selected methodology, binding,
  and schemas from the staged or active release;
- `probe`: run installation and cross-client conformance cases with synthetic or
  explicitly authorized content;
- `activate`: switch the active release using the narrowest reversible native
  mechanism;
- `rollback`: restore the prior validated pointer and adapter configuration;
- `emit_handoff` and `consume_handoff`: exchange the portable handoff envelope
  without credentials or hidden conversation state.

## Adapter Declaration

Each adapter documents:

- supported client/version and protocol release range;
- installation location and immutable package resolution mechanism;
- previous-installation and legacy-guidance discovery mechanism;
- activation atomicity and rollback behavior;
- available access modes and how actual knowledge authorization is enforced;
- capability limitations and checks that must remain `not-run` or
  `not-applicable`;
- exact validation command or client-visible test procedure.

If the client cannot persist an installation pointer, verify source identity,
or isolate old write authority, the adapter may operate per-session in `read` or
`propose` mode but must not claim durable installation or migration readiness.

OpenCode, ChatGPT, and future adapters belong in separate runtime-specific
bindings once their current installation capabilities are verified. Their
mechanics must not be added to the portable core.
