---
protocol: {id: mind-palace, version: 0.1.0}
id: "{{stable-conflict-id}}"
kind: protocol/conflict
title: "Conflict — {{Artifact Title}} — {{Proposal Label}}"
authority: evidence
trust_domain: "{{inherit-source-trust-domain}}"
revision: 1
relations:
  - {type: references, target: "{{conflicted-artifact-id}}"}
provenance:
  - {type: "{{storage-binding}}", locator: "{{conflict-artifact-locator}}"}
---

# Status

**NON-CANONICAL / REQUIRES RECONCILIATION**

# Base

<!-- Artifact ID, logical revision, source version/change token, and digest. -->

# Current

<!-- Current revision/source identity and the material changes since Base. -->

# Proposed Update

<!-- Author/client, timestamp, intended changes, and rationale. -->

# Resolution

<!-- Re-read current state and create a new proposal against it. Never merge automatically. -->
