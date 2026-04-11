---
name: caveman-commit
description: Generate terse, conventional commit messages focusing on why a change was made rather than what changed.
---
# caveman-commit

🪨 Terse commits. Why, not what.

## Instructions

Generate commit messages in Caveman style.

### Rules

1. **Format:** `<type>(<scope>): <subject>` (Conventional Commits).
2. **Subject:** Max 50 chars. No period.
3. **Body:** Only if complex. Use fragments.
4. **Content:** Focus on *why* change made, not *what* changed (code shows what).

### Examples

- `feat(auth): add jwt refresh for session persistence`
- `fix(api): use <= to prevent off-by-one in pagination`
- `docs(readme): add install cmd`
