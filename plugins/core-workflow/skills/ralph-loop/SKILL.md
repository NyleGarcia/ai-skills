---
name: ralph-loop
description: Execute tasks in a continuous, autonomous loop until tests pass or a specific completion condition is met. Integrates tightly with plans/now/todo.md tracking. Use when user wants to run a ralph loop or invokes /ralph-loop.
---

# Ralph Loop

## Quick start

The user wants you to enter an autonomous, self-correcting development loop. Do not stop until the exact completion criteria are met or the maximum iteration limit is reached.

Example trigger: `/ralph-loop "Implement the sorting feature" --completion-promise "All tests pass"`

## Core Principles

1. **Iteration > Perfection**: Don't aim for perfect code on the first try. Let the loop refine the work.
2. **Failures Are Data**: Test failures and linter errors are expected. Use them to debug and self-correct.
3. **Persistence Wins (The `/goal` mindset)**: Keep trying until success. Function as if the `/goal` command was invoked—be extra thorough, do not end your turn to ask for human help unless you've exhausted all options or hit the iteration limit, and do not stop working until the task is completely finished.
4. **Follow Project Management Rules**: Tightly integrate with the `plans/now/todo.md` → `plans/specs/` → `docs/` lifecycle and `gh` CLI syncing as defined in the user's project rules.

## Workflows

When entering a Ralph Loop, immediately follow this procedure:

### Phase 0: The Grill & Sync (Pre-flight check)

Before writing any code, invoke the `/grill-me` mindset:
1. Interview the user relentlessly about their plan, completion promise, and test commands. 
2. Break down the work into discrete, atomic tasks and record them as GitHub issues via `gh` CLI.
3. Sync these issues into `plans/now/todo.md`, ensuring board statuses reflect the new activity.

### Phase 1: Setup

1. **Acknowledge the Loop**: Start your first thought process by declaring "Entering Ralph Loop mode."
2. **Initialize Task Queue**: Read `plans/now/todo.md` to identify the active tasks for this loop.
3. **Initialize State**: Create or update `plans/now/ralph_progress.md` (or draft logic in `plans/specs/`) to track your iterations and test outputs for the current session.

### Phase 1.5: Escalation Assessment (Auto-Trigger Check)

Before executing each task, evaluate it against the escalation triggers below. If **any** trigger fires, **do not attempt solo execution** — immediately delegate to a `teamwork-preview` multi-agent pipeline.

#### Auto-Escalation Triggers

| Trigger | Threshold | Rationale |
|---------|-----------|----------|
| **File spread** | Task touches or is expected to touch >3 files | High coordination cost, multi-agent safer |
| **Cross-layer change** | Task spans ≥2 layers (e.g., BE + FE, DB + API) | Risk of interface mismatch |
| **No verifiable test** | Task has no runnable test command and criteria are subjective | Solo loop can't self-correct without signal |
| **Repeated failure** | Same task failed 3+ times with different fixes | Ralph is stuck; escalate rather than spiral |
| **Explicit user flag** | Task description contains `[teamwork]` or `--delegate` flag | User pre-authorized delegation |

#### Escalation Protocol

1. Log the trigger in `plans/now/ralph_progress.md`: `ESCALATED: <task> — reason: <trigger>`
2. Craft a focused teamwork prompt from the task spec in `plans/specs/`.
3. Invoke `teamwork_preview` subagent via `invoke_subagent` with the prompt.
4. Wait for result. On success: mark task `[x]` in `plans/now/todo.md` and continue Phase 2.
5. On failure: tighten acceptance criteria and re-escalate once before surfacing to user.

### Phase 2: The Loop (Code -> Verify -> Docs -> Repeat)

For each iteration (up to a reasonable limit, default 15 per task):

1. **Fetch Next Task**: Read `plans/now/todo.md`. If all tasks are checked (`[x]`), check if the user has added any new tasks. If the file is fully complete, PROCEED TO PHASE 3. Otherwise, pick the next incomplete `- [ ]` task and mark it as `- [/]` (in progress). Draft implementation details in `plans/specs/`.
2. **Code**: Make the necessary changes to the codebase to implement the feature or fix the bug.
3. **Verify**: Run the verification command (e.g., `npm test`, `pytest`, `cargo test`, `uv run pytest`). 
4. **Analyze**: 
    - If the verification **succeeds** (e.g., exit code 0) and matches the completion promise: Update production truth in `docs/`, check `[x]` in `plans/now/todo.md` (re-linking to `docs/`), update the `gh` project board status, log success in `plans/now/ralph_progress.md`, and REPEAT Phase 2 to pick up the next task.
    - If the verification **fails**: Document the failure in `plans/now/ralph_progress.md`. Formulate a hypothesis for why it failed, apply a fix, and REPEAT Phase 2 for the same task.
5. **Keep Going**: Do **NOT** stop to ask the user for help. Keep executing tool calls (like `run_command` and `replace_file_content`) back-to-back until verification succeeds. 
6. **Multi-Agent Delegation**: See **Phase 1.5** for formal escalation triggers. Any task that hits a trigger is auto-escalated to `teamwork-preview` — do not attempt solo execution past the threshold.


### Phase 3: Completion

1. Once all tasks in `plans/now/todo.md` are marked complete (`[x]`), output a specific completion string or declare success.
2. Archive the plan according to the lifecycle rules, ensuring `gh` project items are fully closed.
3. Let the user know they can append more tasks to `plans/now/todo.md` and run `/ralph-loop` again.
4. Exit the loop and end your turn.

## Advanced features

- **Dynamic Task Refinement**: The user can interrupt you or edit `plans/now/todo.md` directly while the loop is running. Always read `plans/now/todo.md` at the start of every iteration to pick up newly added or refined tasks.
- **Handling Infinite Loops**: If you notice you are trying the exact same fix 3 times in a row without success, step back, document the blockage in `plans/now/ralph_progress.md`, and radically change your approach before continuing the loop.
