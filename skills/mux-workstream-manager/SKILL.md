---
name: mux-workstream-manager
description: Generate WORKSTREAMS.md files for gemini-mux to orchestrate multi-branch development. Use this skill to analyze a project goal, break it down into independent tasks, and create the configuration file required to start a mux session.
---

# Mux Workstream Manager

This skill helps you generate `WORKSTREAMS.md` files for use with `gemini-mux`. It does NOT execute the `gemini-mux` script itself; its sole purpose is to produce the configuration file based on your project needs.

## Workflow

1.  **Analyze the project goal:** Break down the requested feature or bug fix into independent, parallelizable tasks.
2.  **Define branches:** Each task should correspond to a unique git branch name (the `tree` field).
3.  **Draft tasks:** Write concise, actionable prompts for Gemini to execute within each worktree.
4.  **Generate file:** Create the `WORKSTREAMS.md` file in the project root.

## WORKSTREAMS.md Format

The file uses a colon-separated format:
`name:tree:task`

- **name:** A short, friendly name for the tmux window (e.g., `api-fix`).
- **tree:** The name of the git branch/worktree (e.g., `fix-auth-bug`).
- **task:** The prompt Gemini will receive when starting in that worktree.

### Example
```markdown
# WORKSTREAMS.md
auth-logic:feat-auth:Implement JWT rotation in the auth controller and add tests.
ui-login:feat-login-ui:Create a new login page component using Vanilla CSS and React.
db-schema:feat-db:Update the user table to include a last_login_at timestamp.
```

## Best Practices

- **Independence:** Ensure tasks don't have immediate circular dependencies. 
- **Granularity:** Keep tasks small enough to be completed in a single Gemini session.
- **Verification:** Always include "and add/run tests" in the task description.

## Important Note
This skill is for **file generation only**. Once the file is created, you (the user) should run `gemini-mux start` to begin the session.
