---
protocol: {id: mind-palace, version: 0.9.2}
id: "{{stable-reconciliation-report-id}}"
kind: product-engineering/reconciliation-report
methodology: {id: product-engineering, version: 0.2.0}
title: "Reconciliation — {{Project Name}} — {{Date Or Milestone}}"
authority: evidence
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: SUBMITTED
relations:
  - {type: product-engineering/reconciles, target: "{{stable-project-or-baseline-id}}"}
provenance:
  - {type: "{{knowledge-store}}", locator: "{{intent-locator}}"}
  - {type: git, locator: "{{repository-locator}}", source_version: "{{commit-sha}}"}
---

# Evidence Boundary

<!-- Intent revisions and repository/validation identities actually inspected. -->

# Status Map

<!-- Classify items as implemented, partial, absent, planned, deferred, unknown, or drift. -->

# Contradictions And Missing Evidence

<!-- Report conflicts; never silently choose or infer implementation from plans. -->

# Recommended Updates

<!-- Smallest owning-artifact changes; distinguish proposal from applied update. -->
