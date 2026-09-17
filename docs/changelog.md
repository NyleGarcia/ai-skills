---
tags: [changelog, meta]
---

# Changelog

Newest first. One entry per landed task (L1+), Keep-a-Changelog types: Added / Changed / Fixed / Removed.

## 2026-09-17 — housekeeping: dead skills archived, portable paths

- **Removed** (L1): 13 dead skills (`agentic-evolution`, `bootstrap-scorgbot`, `docker-optimize`, `edit-article`, `gemini-api`, `issue-council-report`, `migrate-to-shoehorn`, `qa`, `refactor-pure`, `request-refactor-plan`, `scaffold-exercises`, `subagent-orchestration`, `technical-writing`) moved to `skills/.archived/`, plus `agents/README.md` → `agents/.archived/`. Parked out of skill auto-discovery; contents preserved verbatim.
- **Fixed** (L0): `rules/CLAUDE.md` — skill-security scan tool pointed at a stale macOS path (`/Users/nylegarcia/...`); now `~/git/ai-skills/scripts/scan_skills_security.py`.
- **Changed** (L0): `.gitignore` — `.mcp.json` ignored. MCP server config carries machine-local absolute node/vault paths, so it is local state, not repo state.

## 2026-09-17 — model doctrine: GitHub Actions override

- **Changed** (L1): `rules/CLAUDE.md`, `workflow-standards`, `ci-cd-and-automation`, `cicd-k8s-docker` — GH Actions workflow skills + CI-run watching always `sonnet`/`haiku`, never `opus`/`fable` (watch = haiku, YAML/log triage = sonnet).

## 2026-09-03 — model doctrine: haiku trivial tier

- **Changed** (L1): `workflow-standards` — Model Selection Doctrine split into 4 tiers; new **Trivial** tier (`haiku`, fallback `sonnet`) for zero-judgment one-shot work. Added haiku gate (4 conditions: unique answer, one-shot, inspection-verifiable, fully-specified prompt) and never-haiku list (merge/deploy gates, root-cause, cross-file reasoning). Mechanical tier reworded — invented abbreviations/arrows dropped as fake savings.
- **Changed**: `caveman` skill — levels table (lite/full/ultra), sub-skill specs, negation/number/language-lock preservation rules.
- **Changed** (L1): `workflow-standards` — orchestration split into **Agent Tool (default path)** and **Workflow Tool (opt-in)**. Agent-tool section adds spawn test (3 conditions), agent-type→model picks, ≤4 concurrency + one-message batching + `isolation: worktree` for parallel edits, prompt contract, no-nested-delegation, reuse/reap, producer-never-verifies.
- **Changed**: escalation trigger table inlined, Token Efficiency merged 7→4 bullets — kept file under the 100-line skill cap (99).
- **Added**: `issue-council-report` skill; this `docs/` vault materialized.

## 2026-09-03 — workflow-standards: mandatory docs-closeout gate

- **Changed** (L1): `workflow-standards` skill — docs update + changelog entry now mandatory last step of every task (L1+), same gate as CI green. Checklist: changelog append → repo truth notes → `~/docs` system notes → plans cleanup → skill self-anneal. Silent skip banned (`docs: no impact` required). Ralph-loop/Workflow runs inherit gate.
- **Added** (bootstrap): this `docs/` vault ([[Home]], [[changelog]]) — path refs existed since 15a5044 but vault was never materialized.
