---
protocol:
  id: mind-palace
  version: 0.7.0
id: example-project-product-spec
kind: product-engineering/product-specification
methodology:
  id: product-engineering
  version: 0.2.0
title: Product Specification — Example Project
authority: intent
trust_domain: example
revision: 1
state: APPROVED
relations:
  - type: part_of
    target: example-project
provenance:
  - type: markdown-git
    locator: examples/product-engineering/product-specification.md
---

# Problem And Users

Developers need a non-sensitive example proving the portable artifact format.

# Outcomes And Behavior

The example parses and validates without private knowledge or vendor identity.

# Scope

One representative Product Specification. No storage synchronization.

# Constraints And Principles

Use only synthetic data and portable metadata.

# Acceptance Criteria

- The repository validator accepts this document.
- The document contains no unresolved template placeholders.

# Open Product Questions

None for this example.
