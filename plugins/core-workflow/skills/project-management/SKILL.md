---
name: project-management
description: Integrated project management skill. Merges github-planner, github-project, planning-with-files, and sdlc-delivery. Handles epic planning, board syncing, and todo.md tracking.
---

# Project Management & SDLC

End-to-end orchestration from Epic to Ship.

## 1. SDLC Lifecycle (`sdlc-delivery`)
- **Plans (WIP)**: Mutable `docs/plans/` dir — 3-horizon model: `now/todo.md` (active), `next/backlog.md` (confirmed), `later/ideas.md` (ice box).
- **Specs**: `docs/plans/specs/<slug>.md`, `status: draft | active | done` frontmatter — flip status at closeout, never move/delete (inbound wikilinks depend on the path staying put).
- **Decisions**: `docs/decisions/` for ADR-worthy calls — same vault conventions (frontmatter, wikilinks) as everything else in `docs/`.
- **Docs (Truth)**: Immutable production reference.
- **Pipeline**: `docs/plans/now/todo.md` → `docs/plans/specs/` → code → `docs/` (from spec + diff) → todo line deleted, spec `status: done`.

## 2. GitHub Integration (`github-planner` / `github-project`)
Use `gh` CLI to sync local state with GitHub.
- **Issues**: Slice plan into actionable items. Embed plan links in bodies.
- **Board**: `gh project item-add`. Mutate status via `gh project item-edit`.
- **Items**: Zero orphaned PRs or issues.

## 3. Persistent Tracking (`planning-with-files`)
Strict `todo.md` tracking.
- Master list in `docs/plans/now/todo.md`. Primary link is the tracking issue (`- [ ] <task> ([#123](url))`); add `— [[specs/<slug>]]` once a spec exists for that item — never invent one for a task too small to need it.
- A spec-worthy task goes through `workflow-standards`' Spec Hardening before `/plan` touches it: **Plan** (draft) → **Refine** (`/grill-me`, Obsidian MCP for prior decisions, `graphify` for codebase ground-truth) → **Verify** (fresh-context adversarial pass, never the drafter) → **Fix** (apply findings). Implementation work against that spec — solo, ralph-loop, or Workflow-orchestrated — reads the spec file itself before coding, not just the todo one-liner.
- On completion: check `[x]`, delete the line (the changelog entry is the durable record — see `workflow-standards` Docs Closeout), set the spec's `status: done`.

## 4. Multi-Workstream Orchestration (`mux-workstream-manager`)
Generate `WORKSTREAMS.md` for `gemini-mux`.
- Break complex goals into independent tasks.
- Define branch/window mappings.
