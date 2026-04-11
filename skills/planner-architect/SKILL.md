---
name: planner-architect
description: Workflow for system design, architecture planning, weighing options, creating implementation plans, and managing documentation.
---

# Planner Architect

Use skill to: flush ideas, plan architecture, weigh options, create implementation plans, and manage docs.

## 1. Idea Flush
- Extract core requirements from user.
- Identify constraints, goals, non-goals.
- List potential approaches briefly.

## 2. Architecture & Weighing Options
- Define system components.
- Present 2-3 viable architecture options.
- Weigh pros/cons (trade-offs, DB footprint, speed, cost, maintenance).
- Recommend best option aligned with core optimization goals (e.g., speed, low cost).

## 3. Implementation Plan
- Break chosen architecture into actionable steps.
- Sequence tasks logically (prerequisites first, parallel where possible).
- Keep `plans/` dir up-to-date. `plans/todo.md` is the master index.
- Keep `plans/todo.md` strictly organized + prioritized. Check off completed items. Link from `todo.md` to individual plan files (e.g. `plans/feature.md`) for implementation specifics. Append links to relevant final docs.
- Record parallel planning output in `plans/WORKSTREAMS.md`.
- Generate detailed `implementation_plan` artifact.

## 4. Documentation Management
- Add comprehensive docs for new features/systems.
- Update existing docs (`docs/architecture.md`, `docs/setup.md`, etc.).
- Ensure docs exactly match implementation choices.
- Link newly created/updated docs back to todo items in `plans/todo.md`.

## 5. Project Tracking & Alignment
- **Mandatory Workflow**: ALWAYS use the `github-project` workflow if operating in a repository with a linked GitHub Project board.
- **Create & Link**: Open GitHub issues for planned features and attach them to the board immediately.
- **Capture Stray Work**: Explicitly link loose PRs or unlinked issues via the CLI.
- **Status Mutations**: Update statuses ("In Progress", "In Review", "Done") to map exactly to active implementation phases.
- **Alignment**: Never leave a feature or task undocumented on the board. Project items MUST move through the pipeline to reflect reality.
