---
name: python-dev
description: Expert guidance for Python application development, strictly using uv for dependency management and project isolation. Focuses on src layout, ruff, and pytest.
---

# Python Development Skill

This skill provides expert guidance for building robust, maintainable, and idiomatic Python applications.

## Project Setup & Dependency Management

### Recommended Tools
- **uv**: MANDATORY for lightning-fast package management and project isolation. Never use pip/poetry unless explicitly requested.
- **pytest**: Standard for testing.
- **ruff**: Fast, comprehensive linting and formatting.
- **mypy**: Static type checking.

### Initialization (uv)
```bash
uv init
uv add pytest ruff mypy
```

## Project Structure (src layout)
Prefer the `src/` layout for better test isolation and package integrity:
```
project/
├── pyproject.toml
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

## Coding Standards
- **Type Hinting**: Always use type hints for function signatures and complex variables.
- **Docstrings**: Follow Google or NumPy style docstrings.
- **Asyncio**: Use `async`/`await` for I/O bound tasks.

## Testing with Pytest
- Use fixtures for setup/teardown.
- Place `conftest.py` in the `tests/` directory for shared fixtures.
- Mock external dependencies using `pytest-mock`.

## Common Workflows
- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`
- **Type Checking**: `mypy src`
- **Testing**: `pytest`
