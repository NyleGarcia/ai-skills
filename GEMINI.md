# User Preferences

## Communication Style
- **Mandatory:** Always use `caveman ultra` intensity.
- **Brevity:** Drop filler words and articles. Use telegraphic speech and dev abbreviations.
- **Precision:** Maintain technical accuracy; code blocks must be complete.

## Python Management
- Always use `uv` instead of `pip` for Python dependency management and project isolation.
- Prefer `uv init`, `uv add`, and `uv run` for all Python-related tasks.

## Skills & MCPs
- **Core Directive**: Always use skills and agents where possible.

### Core Engineering & Quality
- `agentic-core`: TDD, refactoring, dependency mgmt, and CLI troubleshooting.
- `agentic-evolution`: Meta-refinement of agents/skills based on history.
- `debugger`: Systematic debugging and error tracing.
- `tdd`: Test-driven development workflows.
- `qa`: Conversational QA and issue filing.
- `security-specialist`: Auditing (static/active) and pre-ship hardening.
- `playwright-e2e`: Automated browser testing.
- `web-quality`: Lighthouse optimization (CWV, Performance, SEO).

### Workflow & Orchestration
- `project-management`: End-to-end SDLC, GitHub Projects sync, and `todo.md`.
- `superpowers`: Execution planning and TDD enforcement.
- `github-triage`: Label-based issue state machine.
- `pr-reviewer`: CLI-based PR reviews.
- `cicd-k8s-docker`: Docker, K8s, and CI/CD pipelines.
- `setup-pre-commit`: Husky and lint-staged configuration.
- `git-guardrails-claude-code`: Blocking dangerous git commands.

### Productivity & Efficiency
- `caveman`: Ultra-compressed communication (commit, review, compress).
- `technical-writing`: Knowledge engine and skill generation.
- `obsidian-vault`: Note management and wikilinks.
- `zoom-out`: High-level perspective and context gathering.
- `write-a-skill`: Creating/updating agent skills.
- `edit-article`: Structural editing and prose tightening.

### Frontend & UI/UX
- `uiux-pro`: Advanced design systems and UI/UX patterns.
- `web-assets`: OG tags, PWA manifests, favicons.
- `frontend`: React/Angular frontend development.
- `humanize-ui`: Strip away the "AI-made" feel from web apps to make them look custom, professional, and trustworthy.

### Backend & Data
- `backend`: FastAPI/Express API development.
- `python-dev`: Expert Python guidance (using `uv`).
- `discord-bot`: Scaffolding for discord.py.
- `alloydb-basics`, `bigquery-basics`, `cloud-run-basics`, `cloud-sql-basics`, `firebase-basics`, `gemini-api`, `gke-basics`: Google Cloud service fundamentals.

### Google Cloud Expert & Agents
- `google-cloud-networking-observability`, `google-cloud-recipe-auth`, `google-cloud-recipe-onboarding`, `google-cloud-waf-cost-optimization`, `google-cloud-waf-reliability`, `google-cloud-waf-security`: Advanced GCP recipes.
- `google-agents-cli-*`: Full lifecycle for Google ADK agents (scaffold, adk-code, eval, deploy, publish, observability, workflow).

### Methodologies
- `design-an-interface`, `domain-model`, `grill-me`, `improve-codebase-architecture`, `js-style-guide`, `migrate-to-shoehorn`, `request-refactor-plan`, `scaffold-exercises`, `to-issues`, `to-prd`, `triage-issue`, `ubiquitous-language`: Specialized software design and process skills.

### Commands
- `/security-review`: Run a security-focused code review on git diff.
- `/refactor:pure`: Refactor current context into a pure function.

### MCP Servers
- `docker`, `docker-docs`, `dockerhub`: Docker ecosystem management.
- `mcp-api-gateway`: Docker-based API integration.
- `node-code-sandbox`: JS execution in Docker.
- `simplechecklist`: Task management with SQLite.

## Project Management Mandates
- **Plans (WIP)**: Mutable `plans/` dir for drafting.
- **Arch (Specs)**: `plans/arch/` for technical design.
- **Docs (Truth)**: Immutable reference of production state.
- **Pipeline**: `plans/todo.md` -> `plans/arch/` -> `plans/features/` -> code -> `docs/` -> archive.
- **Agentic Evolution**: Activate after significant feedback loops to refine toolkit.
- **Tooling**: Always use `sequentialthinking` for complex turns. Vigorously manage `gh` project items.
