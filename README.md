# ai-skills

Centralized repository for AI agent skills and agent definitions, shared across Gemini CLI and Claude Code.

## Structure

- `skills/`: Specialized instructions and domain-specific knowledge (SKILL.md files).
- `agents/`: Custom agent definitions and prompts.

## Installation

Run the provided install script to symlink the skills and agents to their respective configuration directories:

```bash
cd /mnt/d/git/ai-skills
chmod +x install.sh
./install.sh
```

## Compatibility

This repository is designed to be compatible with:
- **Gemini CLI**: Symlinked to `~/.gemini/skills` and `~/.gemini/agents`.
- **Claude Code**: Symlinked to `~/.claude/skills`, `~/.claude-code/skills`, and `~/.agents/skills`.

Any skill added to this repository will be available to both agents simultaneously.
