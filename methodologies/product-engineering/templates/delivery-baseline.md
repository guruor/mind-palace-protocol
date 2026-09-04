---
protocol: {id: mind-palace, version: 0.9.2}
id: "{{stable-baseline-id}}"
kind: product-engineering/delivery-baseline
methodology: {id: product-engineering, version: 0.2.0}
title: "Delivery Baseline — {{Project Name}} — {{Version Or Scope}}"
authority: intent
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: CANDIDATE
relations:
  - {type: part_of, target: "{{stable-project-id}}"}
  - {type: product-engineering/baselines, target: "{{stable-product-spec-id}}"}
  - {type: product-engineering/baselines, target: "{{stable-technical-spec-id}}"}
provenance:
  - {type: "{{storage-binding}}", locator: "{{authoritative-locator}}"}
---

# Frozen Inputs

<!-- For every governing artifact: stable ID, revision, source version or SHA-256 digest. -->

# Current Scope And Non-goals

<!-- Compact references/summary; do not copy whole specifications. -->

# Acceptance And Validation

<!-- Exact criteria and validation expectations governing implementation. -->

# Review Verdict And Human Approval

<!-- Agent verdict, unresolved items, approver, timestamp, and approved revision. -->

# Supersession And Deviation Policy

<!-- What requires a new baseline and how implementation deviations are recorded. -->
