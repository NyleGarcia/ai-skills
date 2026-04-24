---
name: agentic-evolution
description: Refine and enhance agent and skill definitions based on session history, user feedback, and learned patterns. Use when an agent or skill needs to be updated with new principles, tools, or behavioral constraints.
---

# Agentic Evolution

Refine agent personas and skill guides based on empirical usage and feedback.

## Workflow

1.  **Extract Patterns**: Identify recurring instructions, user preferences, or common mistakes from the current session or memory.
2.  **Audit Definition**: Read the target `agents/*.md` or `skills/*/SKILL.md` file.
3.  **Propose Enhancements**:
    *   **Agents**: Add to `Core Principles` or `Responsibilities`.
    *   **Skills**: Update instructions, add references, or refine descriptions.
4.  **Surgical Update**: Apply changes using `replace` or `write_file`.

## Optimization Patterns

### Agent Personas (`agents/*.md`)
*   **Tone Shifts**: If user keeps correcting tone, add a specific bullet to `Core Principles`.
*   **Constraint Injection**: Add "Always use X" or "Never do Y" based on session friction.
*   **Model Tuning**: Suggest switching `model` in frontmatter if performance lags.

### Skill Guides (`skills/*/SKILL.md`)
*   **Trigger Precision**: Refine `description` in frontmatter if the skill triggers too often or too little.
*   **Resource Mapping**: Link new `references/` or `scripts/` added during development.
*   **Brevity Audit**: Remove redundant explanations to save tokens.

## Verification
*   Verify that YAML frontmatter remains valid.
*   Ensure the description is a single-line string.
*   Check that agent `tools` lists are correctly formatted.
