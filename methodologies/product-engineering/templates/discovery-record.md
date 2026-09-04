---
protocol: {id: mind-palace, version: 0.6.0}
id: "{{stable-discovery-id}}"
kind: product-engineering/discovery-record
methodology: {id: product-engineering, version: 0.2.0}
title: "Discovery — {{Topic Or Project}}"
authority: evidence
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: ACTIVE
relations:
  - {type: part_of, target: "{{stable-project-id}}"}
provenance:
  - {type: "{{storage-binding}}", locator: "{{authoritative-locator}}"}
---

# Question Or Opportunity

<!-- What is being explored and what decision/outcome it could change. -->

# Evidence And Observations

<!-- Separate verified facts, source findings, personal observations, and unknowns. -->

# Hypotheses And Options

<!-- Candidate explanations/directions with trade-offs; none are approved by default. -->

# Open Questions

<!-- Include why each matters, example, recommended next evidence, and owner if known. -->

# Promotion Or Parking

<!-- What should enter a spec/decision, remain exploratory, be rejected, or be parked. -->
