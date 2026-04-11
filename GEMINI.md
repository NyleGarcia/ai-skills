# User Preferences

## Communication Style
- **Mandatory:** Always use `caveman ultra` intensity.
- **Brevity:** Drop filler words and articles. Use telegraphic speech and dev abbreviations.
- **Precision:** Maintain technical accuracy; code blocks must be complete.

## Python Management
- Always use `uv` instead of `pip` for Python dependency management and project isolation.
- Prefer `uv init`, `uv add`, and `uv run` for all Python-related tasks.

## Skills & MCPs

### Available Skills
- `caveman`: General brevity. Activate for core communication rules.
- `caveman-commit`: Use for generating terse, conventional commit messages.
- `caveman-review`: Use for providing one-line, emoji-coded code reviews.
- `caveman-compress`: Use to compress prose in memory files (e.g., `GEMINI.md`) to save tokens.
- `python-dev`: Expert Python guidance (dependency management, testing, structure).
- `uiex`: Design system and UI/UX patterns (Vanilla CSS).
- `security-qa`: Security auditing and QA procedures.
- `debugger`: Systematic debugging and error tracing.
- `backend`: Backend API development (FastAPI/Express).
- `frontend`: Frontend development (React/Angular).
- `discord-bot`: Discord bot development with discord.py.
- `cicd-k8s-docker`: Docker, K8s, and CI/CD pipelines.
- `github-planner`: Integrates planner-architect and github-project. Plans architecture, refines issues, links to plan files, tracks on project board.
- `github-project`: Workflow for managing GitHub Projects (V2), creating/linking items, and updating statuses via the gh CLI and issue management.
- `mux-workstream-manager`: Generate WORKSTREAMS.md files for gemini-mux to orchestrate multi-branch development.
- `planner-architect`: Workflow for system design, architecture planning, weighing options, creating implementation plans, and managing documentation.

### Commands
- `/security-review`: Run a security-focused code review on git diff.
- `/refactor:pure`: Refactor current context into a pure function.

### MCP Servers
- `docker`: Execute Docker CLI commands, manage containers/images.
- `docker-docs`: Search/retrieve Docker documentation (Compose, Hub, containerization).
- `dockerhub`: Official Docker Hub MCP. Manage repositories and images.
- `mcp-api-gateway`: Integrate any API using Docker configs.
- `node-code-sandbox`: Spin up disposable Docker containers for JS execution.
- `simplechecklist`: Task management with Docker-optimized SQLite persistence.

## Project Management & Planning
- **`plans/` vs `docs/` Lifecycle:** 
  - `plans/` (WIP): Mutable directory for implementation drafting and `todo.md` tracking.
  - `docs/` (Truth): Immutable reference of production state.
  - Pipeline: `plans/todo.md` -> draft logic in `plans/features/` -> code -> update `docs/` -> check `[x]` in `todo.md` (re-link to `docs/`) -> archive plan.
- **GitHub Projects Syncing:**
  - Create issues for all tasks. Inject links to local `plans/` inside issue descriptions.
  - Vigorously manage project board state via `gh` CLI (`gh project item-add`, `gh project item-edit`). 
  - Board statuses must perfectly reflect branch activity/reality.
