# Antigravity Skills & Agents Toolkit

Master index of all agentic skills loaded in this environment.

## Meta
- **`using-agent-skills`**: Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all other skills are discovered and invoked.

## Define
- **`idea-refine`**: Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on "ideate", "refine this idea", or "stress-test my plan".
- **`interview-me`**: Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified ("build me X" without "for whom" or "why now"), when the user explicitly invokes ("interview me", "grill me", "are we sure?", "stress-test my thinking"), or when you catch yourself silently filling in ambiguous requirements before any plan, spec, or code exists.
- **`spec-driven-development`**: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
- **`to-prd`**: Turn the current conversation context into a PRD and submit it as a GitHub issue. Use when user wants to create a PRD from the current context.

## Plan
- **`planner-architect`**: Workflow for system design, architecture planning, weighing options, creating implementation plans, and managing documentation.
- **`planning-and-task-breakdown`**: Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.
- **`project-management`**: Integrated project management skill. Merges github-planner, github-project, planning-with-files, and sdlc-delivery. Handles epic planning, board syncing, and todo.md tracking.
- **`to-issues`**: Break a plan, spec, or PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into issues.

## Build
- **`alloydb-basics`**: Manages clusters, instances, and backups for AlloyDB for PostgreSQL, and integrates with AlloyDB model context protocol (MCP) tools for automated database operations.
- **`api-and-interface-design`**: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.
- **`backend`**: Backend development expert for Python (FastAPI) and Node.js (Express). Strictly uses uv for Python dependency management.
- **`bigquery-basics`**: Manages datasets, tables, and jobs in BigQuery, and integrates with BigQuery ML and Gemini for advanced data analytics and AI-driven insights. Use when you need to interact with BigQuery, run SQL queries, manage BigQuery resources, or leverage BigQuery's built-in ML capabilities. Also use when performing data analysis, ingesting data into BigQuery, or developing AI applications on BigQuery.
- **`cloud-run-basics`**: Manages Cloud Run services, jobs, and worker pools. Use when you need to deploy applications responding to HTTP requests (services), run event-triggered or scheduled tasks (jobs), or handle always-on pull-based background processing (worker pools).
- **`cloud-sql-basics`**: This file generates or explains Cloud SQL resources. Use this file when the user asks to create a Cloud SQL instance or database for MySQL, PostgreSQL, or SQL Server.
Cloud SQL manages third-party MySQL, PostgreSQL, and SQL Server instances as resources in Cloud SQL. For example, when Cloud SQL creates an open-source MySQL instance, the resulting resource is a Cloud SQL for MySQL instance that Google Cloud manages.
Cloud SQL handles backups, high availability, and secure connectivity for relational database workloads.
- **`context-engineering`**: Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project.
- **`design-an-interface`**: Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice".
- **`discord-bot`**: Comprehensive workflow for Discord bot development with discord.py and interactions.py, focusing on cog architecture, slash commands, and event handling.
- **`doubt-driven-development`**: Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production, security-sensitive logic, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later.
- **`firebase-basics`**: Use this skill whenever you are working on a project that uses Firebase products or services, especially for mobile or web apps.
- **`frontend`**: Frontend development expert for React and Angular using TypeScript and Vanilla CSS. Includes UI/UX patterns from uiux-pro.
- **`frontend-ui-engineering`**: Builds production-quality UIs. Use when building or modifying user-facing interfaces. Use when creating components, implementing layouts, managing state, or when the output needs to look and feel production-quality rather than AI-generated.
- **`gemini-api`**: Guides the usage of the Gemini API on Agent Platform with the Google Gen AI SDK. Use when the user asks about using Gemini in an enterprise environment or explicitly mentions Vertex AI, Google Cloud, or Agent Platform. Covers SDK usage (Python, JS/TS, Go, Java, C#), capabilities like Live API, tools, multimedia generation, caching, and batch prediction.
- **`gke-basics`**: Plan, create, and configure production-ready Google Kubernetes Engine (GKE) clusters using the golden path Autopilot configuration. Covers Day-0 checklist, Autopilot vs Standard, networking (private clusters, VPC-native, Gateway API), security (Workload Identity, Secret Manager, RBAC hardening), observability, scaling, cost optimization, and AI/ML inference. WHEN: create GKE cluster, provision GKE environment, design GKE networking, secure GKE, optimize GKE cost, GKE autoscaling, GKE inference, GKE upgrade, GKE observability, GKE multi-tenancy, GKE batch, GKE HPC, GKE compute class.
- **`incremental-implementation`**: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
- **`python-dev`**: Expert guidance for Python application development, strictly using uv for dependency management and project isolation. Focuses on src layout, ruff, and pytest.
- **`source-driven-development`**: Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters.
- **`tdd`**: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
- **`test-driven-development`**: Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.

## Verify
- **`browser-testing-with-devtools`**: Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data. Requires the chrome-devtools MCP server to be configured.
- **`debugger`**: Systematic debugging workflows, root-cause analysis (RCA), and error tracing for Python and JavaScript.
- **`debugging-and-error-recovery`**: Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error. Use when you need a systematic approach to finding and fixing the root cause rather than guessing.
- **`playwright-e2e`**: Automates web app testing. Claude can test your UI flows end-to-end.
- **`qa`**: Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the background for context and domain language. Use when user wants to report bugs, do QA, file issues conversationally, or mentions "QA session".

## Review
- **`code-review-and-quality`**: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.
- **`code-simplification`**: Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity.
- **`performance-optimization`**: Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vitals or load times need improvement. Use when profiling reveals bottlenecks that need fixing.
- **`pr-reviewer`**: Professional PR reviews with gh CLI.
- **`security-and-hardening`**: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
- **`security-specialist`**: End-to-end security skill. Includes security-qa for static analysis/checklists and security-fuzzer for active vulnerability analysis/endpoint discovery.
- **`web-quality`**: Optimize web projects for Performance, Core Web Vitals, Accessibility, and SEO based on Lighthouse.

## Ship
- **`ci-cd-and-automation`**: Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies.
- **`cicd-k8s-docker`**: Standardized workflows for Docker containerization, Kubernetes orchestration (Helm, manifests), and CI/CD pipelines (GitHub Actions, GitLab CI).
- **`deprecation-and-migration`**: Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code.
- **`documentation-and-adrs`**: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.
- **`domain-model`**: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
- **`git-workflow-and-versioning`**: Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams.
- **`shipping-and-launch`**: Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
- **`web-assets`**: Auto-creates icons, Open Graph tags, PWA assets.

## Meta-Evolution
- **`agentic-evolution`**: Refine and enhance agent and skill definitions based on session history, user feedback, and learned patterns. Use when an agent or skill needs to be updated with new principles, tools, or behavioral constraints.
- **`technical-writing`**: Technical documentation and knowledge management. Merges skill-seekers and tapestry. Auto-generates agent skills and knowledge graphs from raw docs/PDFs.
- **`write-a-skill`**: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.

## Productivity
- **`caveman`**: Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy. Use when user says "caveman mode", "talk like caveman", "use caveman", "less tokens", "be brief", or invokes /caveman.

- **`edit-article`**: Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft.
- **`obsidian-vault`**: Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
- **`zoom-out`**: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits into the bigger picture.

## Methodologies
- **`grill-me`**: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
- **`humanize-ui`**: Strip "AI-made" feel from web apps. Look custom, professional, trustworthy. Use for UI/UX refinement, generic copy fix, AI imagery tweak, bespoke design.
- **`improve-codebase-architecture`**: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable.
- **`js-style-guide`**: Enforce comprehensive JavaScript/TypeScript coding standards based on the Airbnb JavaScript Style Guide. Use for all JS/TS code reviews, refactoring, or authoring.
- **`migrate-to-shoehorn`**: Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.
- **`request-refactor-plan`**: Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps.
- **`scaffold-exercises`**: Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.
- **`triage-issue`**: Triage a bug or issue by exploring the codebase to find root cause, then create a GitHub issue with a TDD-based fix plan. Use when user reports a bug, wants to file an issue, mentions "triage", or wants to investigate and plan a fix for a problem.
- **`ubiquitous-language`**: Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD".
- **`uiux-pro`**: Expert UI/UX design skill integrating impeccable, design-for-ai, ui-ux-pro-max, and claude-design-styles principles.

## Other
- **`agentic-core`**: TDD, debugging, refactoring, dependency mgmt.
- **`git-guardrails-claude-code`**: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
- **`github-triage`**: Triage GitHub issues through a label-based state machine. Use when user wants to create an issue, triage issues, review incoming bugs or feature requests, prepare issues for an AFK agent, or manage issue workflow.
- **`google-agents-cli-adk-code`**: This skill should be used when the user wants to "write agent code", "build an agent with ADK", "add a tool", "create a callback", "define an agent", "use state management", or needs ADK (Agent Development Kit) Python API patterns and code examples. Part of the Google ADK skills suite. It provides a quick reference for agent types, tool definitions, orchestration patterns, callbacks, and state management. Do NOT use for creating new projects (use google-agents-cli-scaffold) or deployment (use google-agents-cli-deploy).

- **`google-agents-cli-deploy`**: This skill should be used when the user wants to "deploy an agent", "deploy my ADK agent", "set up CI/CD", "configure secrets", "troubleshoot a deployment", or needs guidance on Agent Runtime, Cloud Run, or GKE deployment targets. Covers deployment workflows, service accounts, rollback, and production infrastructure. Part of the Google ADK (Agent Development Kit) skills suite. Do NOT use for API code patterns (use google-agents-cli-adk-code), evaluation (use google-agents-cli-eval), or project scaffolding (use google-agents-cli-scaffold).

- **`google-agents-cli-eval`**: This skill should be used when the user wants to "run an evaluation", "evaluate my ADK agent", "write an evalset", "debug eval scores", "compare eval results", or needs guidance on ADK (Agent Development Kit) evaluation methodology and the eval-fix loop. Covers eval metrics, evalset schema, LLM-as-judge, tool trajectory scoring, and common failure causes. Part of the Google ADK (Agent Development Kit) skills suite. Do NOT use for API code patterns (use google-agents-cli-adk-code), deployment (use google-agents-cli-deploy), or project scaffolding (use google-agents-cli-scaffold).

- **`google-agents-cli-observability`**: This skill should be used when the user wants to "set up tracing", "monitor my ADK agent", "configure logging", "add observability", "debug production traffic", or needs guidance on monitoring deployed ADK (Agent Development Kit) agents. Covers Cloud Trace, prompt-response logging, BigQuery Agent Analytics, third-party integrations (AgentOps, Phoenix, MLflow, etc.), and troubleshooting. Part of the Google ADK (Agent Development Kit) skills suite. Do NOT use for deployment setup (use google-agents-cli-deploy) or API code patterns (use google-agents-cli-adk-code).

- **`google-agents-cli-publish`**: This skill should be used when the user wants to "publish an agent", "publish my ADK agent", "register an agent with Gemini Enterprise", "publish to Gemini Enterprise", or needs guidance on the agents-cli publish gemini-enterprise command. Covers ADK vs A2A registration modes, programmatic and interactive usage, flag reference, auto-detection from deployment metadata, and troubleshooting. Part of the Google ADK (Agent Development Kit) skills suite. Do NOT use for deployment (use google-agents-cli-deploy).

- **`google-agents-cli-scaffold`**: This skill should be used when the user wants to "create an agent project", "start a new ADK project", "build me a new agent", "add CI/CD to my project", "add deployment", "enhance my project", or "upgrade my project". Part of the Google ADK (Agent Development Kit) skills suite. Covers `agents-cli scaffold create`, `scaffold enhance`, and `scaffold upgrade` commands, template options, deployment targets, and the prototype-first workflow. Do NOT use for writing agent code (use google-agents-cli-adk-code) or deployment operations (use google-agents-cli-deploy).

- **`google-agents-cli-workflow`**: This skill should be used when the user wants to "develop an agent", "build an agent using ADK", "run the agent locally", "debug agent code", "test an agent", "deploy an agent", "publish an agent", "monitor an agent", or needs the ADK (Agent Development Kit) development lifecycle and coding guidelines. Entrypoint for building ADK agents. Always active — provides the full workflow (scaffold, build, evaluate, deploy, publish, observe), code preservation rules, model selection guidance, and troubleshooting steps for ADK or any agent development.

- **`google-cloud-networking-observability`**: Investigates Google Cloud networking issues by analyzing logs, metrics, and diagnostics. Use when investigating VPC Flow Logs, NAT, firewall, or threat logs, querying latency and throughput metrics, or running Connectivity Tests for path diagnostics.
- **`google-cloud-recipe-auth`**: Provides expert guidance on authenticating and authorizing to Google Cloud services and APIs, covering human users, service identities, Application Default Credentials (ADC), and best practices for secure access.
- **`google-cloud-recipe-onboarding`**: Guidance for a developer's first steps on Google Cloud, covering account creation, billing setup, project management, and deploying a first resource.
- **`google-cloud-waf-cost-optimization`**: Generates cost optimization guidance for Google Cloud workloads based on the Google Cloud Well-Architected Framework (WAF). Use this skill to evaluate a workload, identify cost requirements and constraints, and provide actionable recommendations for build, deploy, and manage the workload cost-efficiently in Google Cloud.
- **`google-cloud-waf-reliability`**: Generates reliability-focused guidance for Google Cloud workloads based on the design principles and recommendations in the Google Cloud Well-Architected Framework. Use this skill to evaluate a workload, identify reliability requirements, and provide actionable recommendations for build, deploy, and manage the workload reliably in Google Cloud.
- **`google-cloud-waf-security`**: Generates security-focused guidance for Google Cloud workloads based on the design principles and recommendations in the Google Cloud Well-Architected Framework (WAF). Use this skill to evaluate a workload, identify security requirements, and provide actionable recommendations for IAM, network security, data protection, and operational security.
- **`setup-pre-commit`**: Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.
- **`superpowers`**: Swiss Army knife for coding. Brainstorming, TDD, execution planning, debugging.

## 🚀 How to Combine
1. `technical-writing` to ingest new tech.
2. `project-management` to plan/sync with GitHub.
3. `superpowers` for TDD execution.
4. `security-specialist` for pre-ship hardening.
5. `agentic-evolution` to improve this toolkit after the session.
