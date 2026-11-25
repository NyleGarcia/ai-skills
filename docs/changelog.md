---
tags: [changelog, meta]
---

# Changelog

Newest first. One entry per landed task (L1+), Keep-a-Changelog types: Added / Changed / Fixed / Removed.

## 2026-11-25 — worktree location rule

- **Changed** (L1): `rules/CLAUDE.md` Git section + `core-workflow:git-workflow-and-versioning` — manual worktrees go under `<repos-root>/worktrees/<repo>-<slug>` (`<repos-root>` = folder holding all git clones, e.g. `~/git`), never as siblings in `<repos-root>`.

## 2026-10-31 — antigravity-offload: deep research

- **Added** (L2): `deep_research` + `research_result` on the `antigravity` MCP server (`~/git/antigravity-mcp` 0.2.0) — background job (plan sub-questions → search + read sources → cross-check → cited Markdown report), `depth` quick/standard/deep, long-poll ≤240 s, one research run at a time. Server merges `read_url(*)` into agy's `settings.json` allow-list at startup: headless agy auto-denies it otherwise, and one denied tool blanks the whole answer (verified on zima).
- **Changed** (L1): `antigravity-offload` — SKILL/REFERENCE cover when to research vs `web_lookup`, prompting, untrusted-report spot-check, failure signatures; `agy_call.py research` starts + polls with local-agy fallback. `rules/CLAUDE.md` Antigravity section lists the tools.

## 2026-10-31 — wizard + tour skills: research pass

- **Changed** (L1): `web-dev:wizard-flow-design` — distilled a UI/UX research brief (CLT, expertise reversal, NN/G wizards, W3C multi-page forms): new step 0 "is a wizard right?" (3–8 steps, <3 → form, >8 → split w/ intermission, Wizard-of-Oz before branch logic), branch pruning, self-sufficient steps, labelled progress rail, no modal over needed data, Review Edit→step→back-to-review, WCAG 2.2 table (title per step, heading focus, fieldset/legend, contrast), expert fast paths, time-on-step + outcome-event metrics, XState guidance, research anti-patterns, extra tests.
- **Changed** (L1): `web-dev:guided-tour-design` — guidance typology (tooltip/hotspot/micro-tour/orientation/launcher/command palette), hybrid micro-tour architecture with hard 5-step cap, self-serve-first triggers + `userIsBusy` gate, learn-by-doing `advanceOn`, per-feature fading after N unaided uses, MutationObserver async-anchor wait with timeout, hotspot pulse ≤5 s, adoption-not-completion metrics, research anti-patterns, extra tests.

## 2026-10-31 — guided-tour-design skill

- **Added** (L1): `web-dev:guided-tour-design` — sibling of `wizard-flow-design` for spotlight/coach-mark tours, page help and first-run walkthroughs (readiness-gated auto-start, public routes explicit, per-tour completion vs opt-out on the user account with localStorage cache + migration, ordered first-match route table with `null` entries, missing-anchor skip, measured/flipping card, focus trap, telemetry); `REFERENCE.md` holds patterns, a bug→rule catalogue from the 2026-10-31 SC-ORG-BOT tour audit, Vitest/RTL recipes and anchor-conformance checks.

## 2026-10-30 — wizard-flow-design + user-testing-guide skills

- **Added** (L1): `web-dev:wizard-flow-design` — multi-step wizard rules (one concern per step, config-gated steps with the old flow pinned, seeded-vs-touched `null`, template rows locked/rebuilt/cleared, close guard + drafts, visible validation, per-target outcomes, field round-trip coverage); `REFERENCE.md` holds patterns, a bug→rule catalogue and test recipes harvested from SC-ORG-BOT's Event/Fleet/LootHub wizards.
- **Added** (L1): `core-workflow:user-testing-guide` — tester-facing guide format (Setup / steps / Expect / Fail if), edge-check checklist, destinations (In-review comment, release note, feedback reply, standing guide); `EXAMPLES.md` from the beta.297 Star Comms retest.

## 2026-10-27 — security-audit: Cloudflare vuln-audit skill vendored

- **Added** (L0): `security:security-audit` — vendored from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (MIT, pin in `UPSTREAM.md`). Six-phase source-first audit (recon → coverage-led hunting → adversarial validation → `findings.json` → record verification → report); guidance mode by default. Zero-dep Node validators, 65/65 tests pass; injection scan clean.

## 2026-10-12 — antigravity-offload: Gemini/image offload with fallback chain

- **Added** (L1): `antigravity-offload` skill — when to hand work to the zima gateway's `antigravity` (images, `ask`) and `agy-bridge` (`web_lookup`, `adversarial_review`, `delegate`, `follow_up`) servers, prompt shapes, gotchas; `REFERENCE.md` with ops/new-machine setup; `scripts/agy_call.py` (stdlib) that speaks streamable-HTTP MCP to the gateway and falls back to a signed-in local `agy`, exit 3 when neither exists.
- **Changed** (L1): `rules/CLAUDE.md` — new "Antigravity offload" section beside Jev: use/don't-use rules and the mandatory fallback (gateway → local agy → WebSearch/own review/say images unavailable). `TOOLKIT.md` lists the skill.

## 2026-09-30 — workflows: `/goal` persistence for long autonomous runs

- **Changed** (L1): `workflow-standards` — new "Persistence — `/goal`" rule under Ralph-Loop & Escalation: L3+ autonomous runs (ralph-loop, multi-turn Workflow/Agent orchestration) pair with Claude Code's built-in `/goal <condition>`, a verifiable end state (tests/lint/build + CI green + docs closeout). User-run, trusted workspace + hooks unrestricted only; 3× same-fix stop rule still applies. Workflow Tool list gains item 5 pointing to it.
- **Changed** (L1): `ralph-loop` — "`/goal` mindset" principle now uses the real command; Phase 1 step 4 turns the completion promise into a `/goal` condition.

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
