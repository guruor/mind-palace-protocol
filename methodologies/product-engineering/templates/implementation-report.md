---
protocol: {id: mind-palace, version: 0.9.1}
id: "{{stable-implementation-report-id}}"
kind: product-engineering/implementation-report
methodology: {id: product-engineering, version: 0.2.0}
title: "Implementation Report — {{Project Name}} — {{Scope}}"
authority: evidence
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: SUBMITTED
relations:
  - {type: product-engineering/implements, target: "{{stable-baseline-id}}"}
provenance:
  - {type: git, locator: "{{repository-locator}}", source_version: "{{commit-sha}}"}
---

# Evidence Boundary

<!-- Repository, branch/PR, base/head/commit identity, environment, and author/client. -->

# Implemented Changes

<!-- Observable behavior and owning components; link to source instead of copying it. -->

# Baseline Coverage

<!-- Map accepted scope/criteria to implementation evidence. -->

# Deviations And Unknowns

<!-- Explicit deviations, incomplete work, skipped areas, and discovered future scope. -->

# Validation Reference

<!-- Link the independent/attributable Validation Report; do not self-approve. -->
