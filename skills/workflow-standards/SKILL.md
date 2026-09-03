---
name: workflow-standards
description: House rules for maximum performance per token — dev lifecycle pipeline (spec→plan→build→test→review→ship→docs), effort-level mapping (L0–L4) from task size to process depth, Workflow/subagent orchestration and model-selection rules, ralph-loop escalation triggers, and token-efficiency principles. Use when starting any non-trivial task, sizing how much process a task deserves, planning multi-agent orchestration, choosing models for subagents, or deciding whether to escalate a stuck loop.
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
plans/now/todo.md → /spec (plans/specs/) → /plan → GH issues (gh CLI, link plans/)
  → /build + ralph-loop (tests/lint/build iterate autonomously)
  → /review → /ship → docs update → check [x] in todo, re-link, remove from now/
```

- **Docs at the end, always:** repo-level truth → that repo's `./docs`; system Linux things (tuning, diag, env) → `~/docs` via `docs-vault`.
- **Board hygiene:** GH Project statuses mirror branch reality — `gh project item-edit` as part of the step, not later.
- **CI gate:** after every push, watch ALL triggered runs to green before calling anything done (global CLAUDE.md one-liner).

## Ralph-Loop & Escalation

Default execution engine for L3+: autonomous code→verify→docs loop on `plans/now/todo.md` (full procedure: `ralph-loop` skill). Stay solo until a trigger fires — solo iteration is the cheapest correct path; escalating without a trigger burns tokens on coordination.

| Auto-escalation trigger | Threshold |
|---|---|
| File spread | task touches >3 files |
| Cross-layer | spans ≥2 layers (BE+FE, DB+API) |
| No verifiable test | no runnable command, subjective criteria |
| Repeated failure | same task failed 3+ with different fixes |
| User flag | `[teamwork]` / `--delegate` in task |

On trigger → four-role pipeline via native Agent tool: **Explorer** (`Explore`, sonnet) → **Worker** (self or opus, local ralph-loop) → **Reviewer** (`code-reviewer`, fable) → **Auditor** (`test-engineer`, fable). Same fix failing 3× in a row = stop, log blockage, change approach radically.

## Orchestration Rules (Workflow + Agent tools)

1. **Opt-in only.** Workflow tool runs only on explicit user request ("use a workflow", ultracode). Otherwise Agent tool or direct.
2. **No agents for trivial work.** L0–L1: never spawn — an agent spawn costs a full context copy; single read/edit/command never pays that back.
3. **Size:** <15 agents per workflow default. Prefer `pipeline()` over flat `parallel()` — verify findings as each review lands; overlap saves wall-clock.
4. **Verify everything:** every reviewer finding gets an adversarial verify agent before reporting. Unverified findings are noise. One good verify pass beats three redundant review passes.
5. **Model roles:** see Model Selection Doctrine below.
6. **Reuse idle agents** via `SendMessage` instead of respawning; kill/collect background agents when done (`subagent-orchestration`).

## Model Selection Doctrine

Core asymmetry: **a worker's mistake gets caught by the verifier; a verifier's mistake ships.** A weak verifier fails silently — you can't tell a review was shallow until prod breaks — so capability concentrates at the gates, and errors get more expensive the further downstream they surface. At equal budget, cheap worker + strong verifier beats strong worker + cheap verifier.

| Tier | Model (fallback) | Roles | Examples |
|------|------------------|-------|----------|
| **Judgment** | `fable` (`opus`) | verifiers, reviewers, auditors, planners — anything whose output gates merge/deploy or sets direction | adversarial verify of findings, code/security review, architecture & spec planning, ralph Reviewer/Auditor, root-cause when stuck, final audit |
| **Production** | `opus` (`sonnet`) | workers — recoverable output that tests + review will catch | implementation, refactoring, debugging w/ repro, test writing, migration execution |
| **Mechanical** | `sonnet` (`haiku` for trivial lookups) | deterministic-ish, low-judgment | fan-out search (Explore), file listing, formatting, boilerplate, status/CI checks, log parsing, schema'd extraction |

Rules:

- **Never downgrade a verifier to save tokens.** Cut budget by downgrading workers or shrinking scope instead.
- **Forced worker downgrade** (opus unavailable) → compensate: bump review one level and/or add a fable verify pass.
- **Upgrade worker → fable** when: task is L4, no verifiable test signal (verifier can't save you), or 3+ failed iterations — being stuck is a judgment problem, not a typing problem.
- **One fable verify pass > several opus passes:** pass-count diversity doesn't close a capability gap on subtle bugs.
- **Ambiguous role?** Classify by blast radius of an unnoticed error: gates something → judgment tier; caught later anyway → production tier.
- Wiring: Agent tool `model` param; Workflow `agent(prompt, {model: 'fable'|'opus'|'sonnet'|'haiku'})`; ralph roles per Ralph-Loop section above.

## Token Efficiency

- **Right-size first:** effort-level classification IS the efficiency mechanism — ceremony scales with stakes, not habit.
- **Cheapest model that can't fail the task;** the one place never to cheap out is verification.
- **Search before read:** grep/glob to locate, then targeted reads (offset/limit). Never dump whole large files into context.
- **Fan-out via Explore agents:** multi-file sweeps go to Explore (sonnet) — conclusions return, file dumps stay out of main context.
- **Don't preload skills:** read a SKILL.md only when the task hits it; descriptions in context are enough for routing.
- **Intermediates in `.tmp/`/scratch,** deliverables to their destination — never round-trip big data through the conversation.
- **Caveman comms** (global rule) already cuts output tokens ~75% — keep it.
