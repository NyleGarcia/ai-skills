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

## Directives
- NEVER refactor without a safety net of tests.
- Isolate side effects. Push I/O to the boundaries of the application.
