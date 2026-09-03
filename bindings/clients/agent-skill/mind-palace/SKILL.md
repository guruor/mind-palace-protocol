---
name: mind-palace
description: Install, validate, retrieve, update, hand off, or migrate durable Mind Palace knowledge and product documentation. Use when the user mentions Mind Palace, common memory, protocol installation, product-document migration, durable knowledge, or cross-client handoff.
compatibility: Requires an authorized common-memory integration for live knowledge operations.
metadata:
  protocol: mind-palace
  adapter-version: "0.1.0"
---

# Mind Palace Bootstrap

1. Resolve common-memory stable ID `mind-palace-protocol-installation`, or an
   explicit instance override. Do not rely on title alone.
2. If it is absent and the user requested installation, follow the immutable
   release's `protocol/common-memory-installation.md`. Otherwise ask for the
   smallest missing installation reference.
3. Verify active protocol version and package identity before using projected
   instructions. Detect same-version identity conflicts and prior/legacy
   installations; never replace them silently.
4. Read the active release's General Guide, selected methodology, and storage
   binding. Load only task-relevant artifacts.
5. Treat common-memory access as separate from write authorization. Preserve
   trust boundaries and remain read-only when effective policy is ambiguous.
6. For migration, require a passing client receipt, source snapshot, mapping,
   omission report, rollback, bounded approval, and immediate pre-write source
   verification.
7. Emit/consume the portable handoff envelope when another client continues the
   work. Never rely on hidden conversation state or embed credentials.

This skill is a discovery adapter, not a copy of the protocol. Existing system,
developer, user, repository, and client instructions remain in force.
