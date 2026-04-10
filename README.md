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
Custom slash commands for both Gemini and Claude.

#### Gemini Format (`.toml`)
Gemini commands support subdirectories. A file at `commands/refactor/pure.toml` is invoked as `/refactor:pure`.
```toml
description = "Description of the command"
prompt = "Prompt instructions..."
```

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

- **Gemini CLI**: Symlinked to `~/.gemini/skills`, `~/.gemini/agents`, and `~/.gemini/commands`.
- **Claude**: Symlinked to `~/.claude/skills`, `~/.claude/agents`, and `~/.claude/commands`.
