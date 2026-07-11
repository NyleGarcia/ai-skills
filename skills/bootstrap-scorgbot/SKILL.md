---
name: bootstrap-scorgbot
description: Scaffolds a new monorepo mirroring the structure, tools, and processes of SC-ORG-BOT.
---

# Bootstrap SC-ORG-BOT Style Monorepo

Use this skill when the user asks to bootstrap a new repository or project like `SC-ORG-BOT` or with a similar complex Python/Node/K8s monorepo setup.

## 1. Directory Structure
Create the foundational directory layout for the monorepo:
```bash
mkdir -p apps packages frontend k8s/charts k8s/overlays/local scripts docs tests
```

## 2. Python Workspace (uv)
Initialize the Python workspace at the root.
Create a `pyproject.toml` containing:
```toml
[project]
name = "my-new-repo"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pydantic-settings",
    "alembic",
    "sqlalchemy",
    "pytest",
    "pytest-asyncio"
]

[tool.uv]
workspace = { members = ["apps/*", "packages/*"] }

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[dependency-groups]
dev = [
    "pre-commit",
    "ruff",
    "mypy",
    "pytest-cov"
]
```
Run `uv sync` to lock dependencies.

## 3. Node & Husky (Semantic Release & Git Hooks)
Initialize `package.json` for frontend and tooling:
```json
{
  "name": "my-new-repo-tooling",
  "version": "0.0.0",
  "private": true,
  "devDependencies": {
    "@semantic-release/changelog": "^6.0.3",
    "@semantic-release/commit-analyzer": "^13.0.1",
    "@semantic-release/git": "^10.0.1",
    "@semantic-release/github": "^12.0.6",
    "@semantic-release/release-notes-generator": "^14.1.0",
    "husky": "^9.1.7",
    "lint-staged": "^17.0.7",
    "prettier": "^3.8.4",
    "semantic-release": "^25.0.3"
  },
  "scripts": {
    "prepare": "husky"
  }
}
```
Run `npm install` and `npx husky init`.

## 4. Pre-commit Configuration
Create `.pre-commit-config.yaml`:
```yaml
repos:
- repo: local
  hooks:
    - id: ruff-check
      name: Lint with Ruff
      entry: uv run ruff check .
      language: system
      pass_filenames: false
      stages: [pre-commit, pre-push]

    - id: ruff-format
      name: Format check with Ruff
      entry: uv run ruff format . --check
      language: system
      pass_filenames: false
      stages: [pre-commit, pre-push]

    - id: mypy
      name: Type check with mypy
      entry: uv run mypy . --ignore-missing-imports
      language: system
      pass_filenames: false
      stages: [pre-commit, pre-push]
```
Run `uv run pre-commit install`.

## 5. Makefile Setup
Create a `Makefile` at the root with standard targets for linting, testing, and k8s:
```makefile
.PHONY: install lint format test build

install:
	uv sync
	npm install

lint:
	uv run ruff check .
	uv run ruff format . --check
	uv run mypy . --ignore-missing-imports

format:
	uv run ruff check . --fix
	uv run ruff format .

test:
	uv run pytest tests/
```

## 6. Execution
- Initialize `git`: `git init`
- Instruct the user on adding apps to `apps/` and packages to `packages/`.
- Ensure everything is tracked.
