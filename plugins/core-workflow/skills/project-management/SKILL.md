---
name: project-management
description: Integrated project management skill. Merges github-planner, github-project, planning-with-files, and sdlc-delivery. Handles epic planning, board syncing, and todo.md tracking.
---

# Project Management & SDLC

End-to-end orchestration from Epic to Ship.

## 1. SDLC Lifecycle (`sdlc-delivery`)
- **Plans (WIP)**: Mutable `docs/plans/` dir — 3-horizon model: `now/` (active), `next/` (backlog), `later/` (ideas).
- **Specs**: `docs/plans/specs/` for technical design docs.
- **Docs (Truth)**: Immutable production reference.
- **Pipeline**: `docs/plans/now/todo.md` → `docs/plans/specs/` → code → `docs/` → remove from `now/`.

## 2. GitHub Integration (`github-planner` / `github-project`)
Use `gh` CLI to sync local state with GitHub.
- **Issues**: Slice plan into actionable items. Embed plan links in bodies.
- **Board**: `gh project item-add`. Mutate status via `gh project item-edit`.
- **Items**: Zero orphaned PRs or issues.

## 3. Persistent Tracking (`planning-with-files`)
Strict `todo.md` tracking.
- Master list in `docs/plans/now/todo.md`.
- Link tasks to specific plan files or final docs.

## 4. Multi-Workstream Orchestration (`mux-workstream-manager`)
Generate `WORKSTREAMS.md` for `gemini-mux`.
- Break complex goals into independent tasks.
- Define branch/window mappings.
