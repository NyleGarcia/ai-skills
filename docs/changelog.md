---
tags: [changelog, meta]
---

# Changelog

Newest first. One entry per landed task (L1+), Keep-a-Changelog types: Added / Changed / Fixed / Removed.

## 2026-09-03 — workflow-standards: mandatory docs-closeout gate

- **Changed** (L1): `workflow-standards` skill — docs update + changelog entry now mandatory last step of every task (L1+), same gate as CI green. Checklist: changelog append → repo truth notes → `~/docs` system notes → plans cleanup → skill self-anneal. Silent skip banned (`docs: no impact` required). Ralph-loop/Workflow runs inherit gate.
- **Added** (bootstrap): this `docs/` vault ([[Home]], [[changelog]]) — path refs existed since 15a5044 but vault was never materialized.
