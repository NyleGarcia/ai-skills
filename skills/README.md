# Agentic Skills & Agents Toolkit

Master index of all agentic skills loaded in this environment.

## Quick Index

| Category | Skills |
|----------|--------|
| **Meta** | `using-agent-skills` |
| **Define** | `interview-me`, `idea-refine`, `spec-driven-development`, `to-prd` |
| **Plan** | `planning-and-task-breakdown`, `planner-architect`, `project-management`, `to-issues` |
| **Build** | `incremental-implementation`, `context-engineering`, `source-driven-development`, `doubt-driven-development`, `frontend-ui-engineering`, `test-driven-development`, `api-and-interface-design`, `design-an-interface` |
| **Verify** | `browser-testing-with-devtools`, `debugging-and-error-recovery`, `playwright-e2e`, `qa` |
| **Review** | `code-review-and-quality`, `code-simplification`, `security-and-hardening`, `security-specialist`, `performance-optimization`, `pr-reviewer`, `web-quality` |
| **Ship** | `git-workflow-and-versioning`, `ci-cd-and-automation`, `cicd-k8s-docker`, `deprecation-and-migration`, `documentation-and-adrs`, `domain-model`, `shipping-and-launch`, `web-assets` |
| **Meta-Evolution**| `agentic-evolution`, `write-a-skill`, `technical-writing`, `subagent-orchestration` |
| **Productivity** | `caveman`, `obsidian-vault`, `zoom-out`, `edit-article` |
| **Backend/Data** | `backend`, `python-dev`, `discord-bot`, `alloydb-basics`, `bigquery-basics`, etc. |
| **Methodologies** | `grill-me`, `js-style-guide`, `migrate-to-shoehorn`, `request-refactor-plan`, `scaffold-exercises`, `triage-issue`, `ubiquitous-language` |

## Detailed Manual
See [TOOLKIT.md](./TOOLKIT.md) for detailed descriptions and combined workflows.

## Development
To add a new skill, use the `write-a-skill` skill:
1. Create a directory `skills/my-new-skill`.
2. Add `SKILL.md` with YAML frontmatter.
3. Update `GEMINI.md` and `TOOLKIT.md`.
