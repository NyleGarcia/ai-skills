---
name: github-project
description: Workflow for managing GitHub Projects (V2), creating/linking items, and updating statuses via the gh CLI and issue management.
---

# GitHub Project Management

This skill defines the structured workflow for interacting with GitHub Projects, ensuring designated project boards are kept in sync with development.

Since the `github-mcp-server` does not natively support Project board V2 manipulation, we aggressively employ the `gh` (GitHub CLI) via `run_command`.

## Core Tasks

### 1. Identify Target Project
Always confirm the target project number first by querying the org/user owner.
```bash
# turbo
gh project list --owner <owner>
```

### 2. Creating New Items (Issues + Project Link)
When creating a planned feature, first create the underlying issue, then link it to the project.
1. Formulate the issue and create it with the `issue_write` MCP tool (or `gh issue create`).
2. Capture the returned issue URL.
3. Link the issue URL to the board:
```bash
gh project item-add <project_number> --owner <owner> --url "<issue_url>"
```

### 3. Linking Existing Work
When taking on existing work (like a stray PR or an unlinked Issue), explicitly add it:
```bash
gh project item-add <project_number> --owner <owner> --url "<pull_request_or_issue_url>"
```

### 4. Updating Item Status
To mark an item as "In Progress", "In Review", or "Done", you must interact with the project's custom fields.
*Step 1: Retrieve items to get the Item ID.*
```bash
gh project item-list <project_number> --owner <owner> --format json
```
*Step 2: List project fields and capture the exact ID for the 'Status' field and its option IDs.*
```bash
gh project field-list <project_number> --owner <owner>
```
*Step 3: Mutate the item state.*
```bash
gh project item-edit --id "<item_id>" --project-id "<project_global_id>" --field-id "<status_field_id>" --single-select-option-id "<target_status_option_id>"
```

## Caveman Rules
- Never guess the IDs; always fetch them via `gh project` lists if they aren't fresh in memory.
- Automate this silently in the background when closing out user tasks.
- Keep board matching the active project's workstreams.
