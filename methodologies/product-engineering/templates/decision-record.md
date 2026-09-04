---
protocol: {id: mind-palace, version: 0.7.0}
id: "{{stable-decision-id}}"
kind: product-engineering/decision-record
methodology: {id: product-engineering, version: 0.2.0}
title: "Decision — {{Imperative Decision Title}}"
authority: history
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: PROPOSED
relations:
  - {type: part_of, target: "{{stable-project-id}}"}
provenance:
  - {type: "{{storage-binding}}", locator: "{{authoritative-locator}}"}
---

# Context

<!-- The concrete problem, constraints, evidence, and why a decision is needed now. -->

# Decision

<!-- The chosen direction. Keep one material decision per record. -->

# Alternatives And Trade-offs

<!-- Only materially different options and why they were not selected. -->

# Consequences

<!-- Positive/negative outcomes, risks, required follow-ups, and reversibility. -->

# Status And Supersession

<!-- Approval/rejection/deferral evidence and links to decisions this supersedes. -->
