---
name: workflow-standards
description: House rules for maximum performance per token — dev lifecycle pipeline (spec→plan→build→test→review→ship→docs), mandatory docs-closeout gate ending every task, effort-level mapping (L0–L4) from task size to process depth, Workflow/subagent orchestration and model-selection rules, ralph-loop escalation triggers, and token-efficiency principles. Use when starting any non-trivial task, sizing how much process a task deserves, planning multi-agent orchestration, choosing models for subagents, deciding whether to escalate a stuck loop, or closing out a task.
---

# Workflow Standards

How work moves through this environment, tuned for best bang-for-buck (quality per token). First step of any task: classify effort level, then run only the process that level demands — no more, no less. Over-processing small tasks is the #1 token waste.

## Effort Levels

| Lvl | Signals | Process | Agents / Orchestration | Review |
|-----|---------|---------|------------------------|--------|
| **L0 trivial** | typo, config tweak, one-liner, lookup | direct edit, no ceremony | none — do it yourself | self-check + tests if logic touched |
| **L1 small** | single-file bug/feature, clear repro | `test-driven-development` (red→green), direct | none | `/code-review low` |
| **L2 medium** | multi-file feature, refactor, ~1 session | `/plan` → `/build` (incremental) → `/test` | Explore agents ok (sonnet); no Workflow | `/code-review medium`–`high` |
| **L3 large** | new feature/system, multi-day, parallelizable | `/spec` → `/plan` → `to-issues` → `/ralph-loop` | Workflow if user opted in (<15 agents); roles per model table | `/code-review high` + fable verify pass |
| **L4 critical** | prod deploy, security, migrations, irreversible | L3 + `doubt-driven-development` + `security:security-review` | fable verifiers mandatory, never skipped | `/code-review max` or `ultra`; `/ship` checklist |

Escalate a level when: unfamiliar code, prod-facing, or being confidently wrong would cost more than the extra process. Never silently de-escalate mid-task.

## Lifecycle Pipeline

```
docs/plans/now/todo.md → /spec (docs/plans/specs/) → /plan → GH issues (gh CLI, link docs/plans/)
  → /build + ralph-loop (tests/lint/build iterate autonomously)
  → /review → /ship → docs closeout (see below) → check [x] in todo, re-link, remove from now/
```

- **Board hygiene:** GH Project statuses mirror branch reality — `gh project item-edit` as part of the step, not later.
- **CI gate:** after every push, watch ALL triggered runs to green before calling anything done (global CLAUDE.md one-liner).

## Docs Closeout — Mandatory Last Step

Every task L1+ ends with a docs pass before it counts as done — same gate as CI green. L0 too if it changed behavior/config anyone else relies on. Run the checklist top to bottom:

1. **Changelog, always:** append entry to that repo's `docs/changelog.md` (create if missing; newest first, Keep-a-Changelog style): `## YYYY-MM-DD — <one-line summary>` + type (`Added/Changed/Fixed/Removed`), effort level, wikilinks to touched truth notes/specs, PR/issue refs.
2. **Repo truth changed** (arch, API, ADR-worthy decision, new skill/script)? → update that repo's `./docs` note(s) + `docs/Home.md` index (`docs-vault` conventions).
3. **System/env fix** (Linux tuning, diag, setup, handoff)? → note in `~/docs` + `~/docs/Home.md` index.
4. **Plans:** check `[x]` in `docs/plans/now/todo.md`, re-link via wikilink to truth note, remove from `now/`; archive/close spec.
5. **Skill learned constraint/edge case?** → self-anneal: update relevant `SKILL.md`.

Changelog entry (step 1) never skipped for L1+. Steps 2–5: if nothing applies, state `docs: no impact` explicitly — silent skip not allowed. Ralph-loop and Workflow runs inherit this gate: final iteration includes docs closeout before reporting done.

## Ralph-Loop & Escalation

Default execution engine for L3+: autonomous code→verify→docs loop on `docs/plans/now/todo.md` (full procedure: `ralph-loop` skill). Stay solo until a trigger fires — solo iteration is the cheapest correct path; escalating without a trigger burns tokens on coordination.

**Auto-escalate triggers** (any one): task touches >3 files · spans ≥2 layers (BE+FE, DB+API) · no runnable verification / subjective criteria · same task failed 3+ times with different fixes · user flags `[teamwork]` or `--delegate`.

On trigger → four-role pipeline via native Agent tool: **Explorer** (`Explore`, sonnet) → **Worker** (self or opus, local ralph-loop) → **Reviewer** (`code-reviewer`, fable) → **Auditor** (`test-engineer`, fable). Same fix failing 3× in a row = stop, log blockage, change approach radically.

## Orchestration — Agent Tool (default path)

Workflow tool is opt-in; every other delegation lands here — or stays solo, which is the cheapest correct path.

- **Spawn test — all three, else do it yourself:** (1) separable scope, no shared-file writes; (2) return is a conclusion, not a dump you'd re-read anyway; (3) worth a full context copy — that's what a spawn costs. L0–L1, single read/edit/grep, or a fact you know where to find: never spawn.
- **Agent picks (type, model):** fan-out search → `Explore` (sonnet) · unknown-shape research → `general-purpose` (opus) · review gate → `code-reviewer` (fable) · tests → `test-engineer` (opus; fable if it gates merge) · security → `security:security-auditor` (fable) · architecture/plan → `Plan` (fable) · needs your exact context → `fork` (inherits your model, override ignored) · trivial lookup/listing → `general-purpose` (haiku, per haiku gate).
- **Concurrency:** ≤4 concurrent default (L3+ more, user opt-in). Independent spawns go in ONE message — one spawn per turn wastes a turn each. Never two agents writing the same file; parallel edits need `isolation: worktree`.
- **Prompt contract:** exact scope, exact paths/commands, explicit return shape (`file:line + one-line claim`), and "report conclusions, not file contents". Vague prompt = agent burns a context rediscovering what you already knew.
- **No nested delegation.** Subagent doesn't spawn subagents; a fork executes directly. Depth multiplies context copies, adds no verifier.
- **Reuse + reap:** `SendMessage` an idle agent instead of respawning (context already warm); collect/kill background agents when done (`subagent-orchestration`). Never fabricate a pending agent's result — wait for the notification, and treat returned findings as claims to check, not facts.
- **Producer never verifies:** the agent that found it doesn't confirm it. Fresh-context adversarial verify (fable) or the finding stays unreported.

## Orchestration — Workflow Tool (opt-in only)

1. **Explicit request only** ("use a workflow", ultracode, or a skill that says to). Otherwise Agent tool or direct.
2. **Size:** <15 agents default. `pipeline()` over flat `parallel()` — verify findings as each review lands; overlap saves wall-clock.
3. **Verify everything:** every finding gets an adversarial verify agent. Unverified findings are noise; one good verify pass beats three redundant review passes.
4. **Model roles:** Model Selection Doctrine below. Same spawn test and prompt contract as Agent tool apply per-agent.

## Model Selection Doctrine

Core asymmetry: **a worker's mistake gets caught by the verifier; a verifier's mistake ships.** A weak verifier fails silently — you can't tell a review was shallow until prod breaks — so capability concentrates at the gates, and errors get more expensive the further downstream they surface. At equal budget, cheap worker + strong verifier beats strong worker + cheap verifier.

| Tier | Model (fallback) | Roles | Examples |
|------|------------------|-------|----------|
| **Judgment** | `fable` (`opus`) | verifiers, reviewers, auditors, planners — anything whose output gates merge/deploy or sets direction | adversarial verify of findings, code/security review, architecture & spec planning, ralph Reviewer/Auditor, root-cause when stuck, final audit |
| **Production** | `opus` (`sonnet`) | workers — recoverable output that tests + review will catch | implementation, refactoring, debugging w/ repro, test writing, migration execution |
| **Mechanical** | `sonnet` (`haiku` if shape is fully specified) | deterministic-ish, low-judgment, still needs some reading comprehension | fan-out search (Explore), boilerplate, refactor-by-pattern, log parsing, schema'd extraction |
| **Trivial** | `haiku` (`sonnet`) | zero-judgment, one-shot, verifiable at a glance — output is right or obviously wrong | single-fact lookup, file/dir listing, formatting & lint-fix, status/CI/PR checks, git metadata, string/JSON reshaping, yes-no existence checks |

Rules:

- **Never downgrade a verifier to save tokens.** Cut budget by downgrading workers or shrinking scope instead.
- **Forced worker downgrade** (opus unavailable) → compensate: bump review one level and/or add a fable verify pass.
- **Upgrade worker → fable** when: task is L4, no verifiable test signal (verifier can't save you), or 3+ failed iterations — being stuck is a judgment problem, not a typing problem.
- **One fable verify pass > several opus passes:** pass-count diversity doesn't close a capability gap on subtle bugs.
- **Haiku gate — all four or step up to sonnet:** (1) no design choice — the right answer is unique; (2) task is one-shot, no multi-step plan; (3) output is verifiable by inspection or a command; (4) prompt carries the full spec (exact paths, exact format) — haiku won't infer intent from a vague ask.
- **Never haiku for:** anything that gates merge/deploy, root-cause work, cross-file reasoning, or a prompt you'd have to think about yourself. A retry loop on haiku costs more than sonnet first try.
- **Ambiguous role?** Classify by blast radius of an unnoticed error: gates something → judgment tier; caught later anyway → production tier.
- Wiring: Agent tool `model` param; Workflow `agent(prompt, {model: 'fable'|'opus'|'sonnet'|'haiku'})`; ralph roles per Ralph-Loop section above.

## Token Efficiency

- **Right-size first:** effort classification IS the efficiency mechanism — ceremony scales with stakes, not habit. Cheapest model that can't fail the task; never cheap out on verification.
- **Search before read:** grep/glob to locate, then targeted reads (offset/limit) — never dump whole files. Multi-file sweeps go to `Explore`: conclusions return, dumps stay out of main context.
- **Don't preload skills:** read a SKILL.md only when the task hits it; descriptions in context route fine.
- **Intermediates in `.tmp/`/scratch,** deliverables to their destination — never round-trip big data through the conversation. Caveman comms (global rule) stays on.
