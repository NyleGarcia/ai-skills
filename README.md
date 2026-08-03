# ai-skills

Centralized repository for AI agent skills, definitions, and custom commands.

## Structure

### Skills
Each skill is organized into a directory following this structure:
```
my-skill/
├── SKILL.md       (Required) Instructions and metadata
├── scripts/       (Optional) Executable scripts
├── references/    (Optional) Static documentation
└── assets/        (Optional) Templates and other resources
```

### Commands (`commands/`)
Custom slash commands for Claude.

#### Claude Format (`.md`)
Claude commands use Markdown with YAML frontmatter.
```markdown
---
description: Run a security-focused code review
allowed-tools:
  - Bash(git diff:*)
---
## Task
Instructions here...
```

### Other Directories
- `agents/`: Custom agent definitions and prompts.

## Installation

Run the provided install script to backup existing local data, merge it into the repository, and setup symlinks:

```bash
cd /mnt/d/git/ai-skills
chmod +x install.sh
./install.sh
```

## Compatibility

- **Claude**: Symlinked to `~/.claude/skills`, `~/.claude/agents`, `~/.claude/commands`, and `~/.claude/CLAUDE.md` (see `rules/CLAUDE.md`). `plugins/` is registered as a local Claude Code marketplace (`.claude-plugin/marketplace.json` at the repo root) and each plugin is installed via `claude plugin install <name>@ai-skills`. Each plugin's manifest lives at `plugins/<name>/.claude-plugin/plugin.json`.
