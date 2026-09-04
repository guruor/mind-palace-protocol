---
protocol: {id: mind-palace, version: 0.9.2}
id: "{{stable-validation-report-id}}"
kind: product-engineering/validation-report
methodology: {id: product-engineering, version: 0.2.0}
title: "Validation Report — {{Project Name}} — {{Scope}}"
authority: evidence
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: SUBMITTED
relations:
  - {type: product-engineering/validates, target: "{{stable-implementation-report-or-baseline-id}}"}
provenance:
  - {type: "{{evidence-provider}}", locator: "{{evidence-locator}}"}
---

# Evidence Boundary

<!-- Exact source revision, environment, tools, permissions, and unavailable evidence. -->

# Validation Results

<!-- Commands/checks, expected behavior, result, and compact attributable evidence. -->

# Failures, Skips, And Limitations

<!-- A skipped check is not a pass. Explain consequence and required follow-up. -->

# Verdict

<!-- One evidence-backed verdict and the exact artifact/source revision it covers. -->
