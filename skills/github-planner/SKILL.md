---
name: github-planner
description: Integrates planner-architect and github-project. Plans architecture, refines issues, links to plan files, tracks on project board.
---

# GitHub Planner

Merge `planner-architect` rigor with `github-project` tracking.

## 1. Architect & Plan
- Extract reqs. Define constraints.
- Draft implementation plan.
- Keep `plans/` dir up-to-date. `plans/todo.md` is master list: organized and prioritized.
- Check off done tasks in `todo.md`. Link out to specific plan files (e.g., `plans/native-discord-sync.md`) for implementation specifics, and to final docs when complete.
- Update `plans/WORKSTREAMS.md`.

## 2. Issue Refinement & File Linking
- Slice plan into actionable GitHub issues.
- Detail tasks, acceptance criteria.
- **Crucial:** Embed links/references to config & plan files in issue body.
- Update local plan files with generated issue URLs.

## 3. Board Sync (CLI)
- Create issue (`issue_write` or `gh issue create`).
- Link to board: `gh project item-add <proj_id> --url <issue_url>`.
- Mutate status via `gh project item-edit`. 
- Ensure zero orphaned PRs/issues.
