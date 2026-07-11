---
name: agentic-core
description: TDD, debugging, refactoring, dependency mgmt.
---

# Agentic Core Engineering

Base engineering framework for autonomous execution.

## Core Capabilities
- **Refactoring:** Identify code smells (Long Method, God Class). Extract modules systematically ensuring tests pass.
- **Dependency Mgmt:** Use `uv` (Python), `npm/yarn/pnpm` (JS) to lock dependencies. Audit for CVEs.
- **TDD:** Strict test-first approach.
- **Debugging:** Formulate hypothesis -> Write failing test reproducing bug -> Implement fix -> Verify test passes.

## CLI Troubleshooting & Mastery
- **Interactive Timeouts:** If a command hangs waiting for an editor (e.g., `git rebase`, `git commit --amend`), prefix with `GIT_EDITOR=true` or use non-interactive flags.
- **SSL/Network Issues:** If `git push/pull` fails with SSL certificate errors in restricted environments, temporarily use `git -c http.sslVerify=false` if authorized, or verify system time.
- **Detached HEAD/Conflicts:** Always `git status` before and after complex operations. Resolve conflicts by reading markers, writing fixed files, and `git add`.
- **Background Processes:** Use `is_background: true` for servers/watchers; use `read_background_output` to check progress.

## Directives
- NEVER refactor without a safety net of tests.
- Isolate side effects. Push I/O to the boundaries of the application.
- Prefer `GIT_EDITOR=true` for all automated git mutations.
