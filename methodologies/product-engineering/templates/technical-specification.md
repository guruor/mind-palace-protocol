---
protocol: {id: mind-palace, version: 0.9.3}
id: "{{stable-technical-spec-id}}"
kind: product-engineering/technical-specification
methodology: {id: product-engineering, version: 0.2.0}
title: "Technical Specification — {{Project Name}}"
authority: intent
trust_domain: "{{configured-trust-domain}}"
revision: 1
state: DRAFT
relations:
  - {type: part_of, target: "{{stable-project-id}}"}
  - {type: references, target: "{{stable-product-spec-id}}"}
provenance:
  - {type: "{{storage-binding}}", locator: "{{authoritative-locator}}"}
---

# Context And Constraints

<!-- Product baseline, existing system, ownership, security, and compatibility. -->

# Architecture And Data Flow

<!-- Intended design and boundaries. This does not prove current implementation. -->

# Interfaces And Persistence

<!-- Contracts, state, versions, migrations, failure behavior, and dependencies. -->

# Alternatives And Decisions

<!-- Important trade-offs; link a Decision Record when rationale merits one. -->

# Validation Strategy

<!-- Cheapest meaningful deterministic and behavioral validation tiers. -->

# Rollout, Recovery, And Risks

<!-- Reversibility, partial failure, compatibility, operational and privacy risks. -->

# Deferred Scope And Open Questions

<!-- Preserve but do not silently promote future work. -->
