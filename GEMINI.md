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
- `caveman-commit`: Terse, conventional commit messages. Use for git history hygiene.
- `caveman-review`: One-line, emoji-coded code reviews.
- `caveman-compress`: Compress prose in memory files to save tokens.
- `python-dev`: Python guidance (dependencies, testing, structure).
- `uiex`: Design system and UI/UX patterns (Vanilla CSS).
- `uiux-pro`: Advanced design system generator. Use to fight generic LLM UI bias.
- `security-qa`: Static analysis and QA procedures. Use for codebase hardening.
- `security-fuzzer`: Active vulnerability analysis. Use for endpoint discovery and fuzzing.
- `debugger`: Systematic debugging. Use for root-cause analysis.
- `backend`: Backend API development (FastAPI/Express).
- `frontend`: Frontend development (React/Angular).
- `discord-bot`: Discord bot development with discord.py.
- `cicd-k8s-docker`: Docker, K8s, and CI/CD pipelines.
- `superpowers`: Swiss army knife. Use for TDD enforcement, brainstorming, and execution planning.
- `planning-with-files`: Manus-style persistence. Use for strict `todo.md` tracking on complex epics.
- `agentic-core`: Base framework. Use for deep refactoring and systematic dependency mgmt.
- `sdlc-delivery`: Full lifecycle orchestration. Use for epic planning through release notes.
- `web-quality`: Lighthouse optimization. Use to fix Core Web Vitals, a11y, SEO, and perf.
- `web-assets`: Asset generation. Use to build PWA manifests, OG tags, favicons.
- `playwright-e2e`: Automated browser testing. Use for UI flow validation.
- `skill-seekers`: Skill generator. Use to convert raw framework docs/repos into AI knowledge assets.
- `tapestry`: Knowledge graph builder. Use to convert PDFs and API docs into navigable markdown.
- `pr-reviewer`: Pull request audits. Use with `gh` CLI for rigorous pre-merge checks.
- `using-agent-skills`: Meta-skill for skill discovery.
- `spec-driven-development`: Spec before code.
- `planning-and-task-breakdown`: Small, atomic tasks.
- `incremental-implementation`: One vertical slice at a time.
- `test-driven-development`: Tests are proof.
- `code-review-and-quality`: Improve code health.
- `code-simplification`: Clarity over cleverness.
- `shipping-and-launch`: Faster is safer.
- `debugging-and-error-recovery`: Systematic root-cause debugging.
- `security-and-hardening`: Hardens code against vulnerabilities.
- `performance-optimization`: Optimize for speed and efficiency.
- `browser-testing-with-devtools`: Runtime verification in Chrome.
- `frontend-ui-engineering`: Specialized UI workflows.
- `api-and-interface-design`: Designing robust APIs.
- `git-workflow-and-versioning`: Clean git history and branching.
- `ci-cd-and-automation`: Robust pipelines.
- `deprecation-and-migration`: Safely moving off legacy code.
- `documentation-and-adrs`: Capturing architectural decisions.
- `context-engineering`: Managing prompt context and knowledge.
- `doubt-driven-development`: Defensive engineering in high-stakes areas.
- `source-driven-development`: Code verified against documentation.
- `interview-me`: Requirements gathering via interview.
- `idea-refine`: Expanding and refining rough concepts.

### Lifecycle Commands
- `/spec` -> `spec-driven-development`
- `/plan` -> `planning-and-task-breakdown`
- `/build` -> `incremental-implementation`
- `/test` -> `test-driven-development`
- `/review` -> `code-review-and-quality`
- `/code-simplify` -> `code-simplification`
- `/ship` -> `shipping-and-launch`

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
