---
tags: [changelog, meta]
---

# Changelog

Newest first. One entry per landed task (L1+), Keep-a-Changelog types: Added / Changed / Fixed / Removed.

## 2026-09-03 — model doctrine: haiku trivial tier

- **Changed** (L1): `workflow-standards` — Model Selection Doctrine split into 4 tiers; new **Trivial** tier (`haiku`, fallback `sonnet`) for zero-judgment one-shot work. Added haiku gate (4 conditions: unique answer, one-shot, inspection-verifiable, fully-specified prompt) and never-haiku list (merge/deploy gates, root-cause, cross-file reasoning). Mechanical tier reworded — invented abbreviations/arrows dropped as fake savings.
- **Changed**: `caveman` skill — levels table (lite/full/ultra), sub-skill specs, negation/number/language-lock preservation rules.
- **Added**: `issue-council-report` skill; this `docs/` vault materialized.

## 2026-09-03 — workflow-standards: mandatory docs-closeout gate

- **Changed** (L1): `workflow-standards` skill — docs update + changelog entry now mandatory last step of every task (L1+), same gate as CI green. Checklist: changelog append → repo truth notes → `~/docs` system notes → plans cleanup → skill self-anneal. Silent skip banned (`docs: no impact` required). Ralph-loop/Workflow runs inherit gate.
- **Added** (bootstrap): this `docs/` vault ([[Home]], [[changelog]]) — path refs existed since 15a5044 but vault was never materialized.
