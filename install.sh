#!/usr/bin/env bash

# ai-skills/install.sh - Symlink Gemini and Claude skills/agents

REPO_DIR=$(pwd)

# Gemini paths
GEMINI_SKILLS_PATH="$HOME/.gemini/skills"
GEMINI_AGENTS_PATH="$HOME/.gemini/agents"

# Claude paths
CLAUDE_SKILLS_PATH="$HOME/.claude/skills"
CLAUDE_CODE_SKILLS_PATH="$HOME/.claude-code/skills"
AGENTS_SKILLS_PATH="$HOME/.agents/skills"

# Symlink Gemini
mkdir -p "$HOME/.gemini"
rm -rf "$GEMINI_SKILLS_PATH" "$GEMINI_AGENTS_PATH"
ln -s "$REPO_DIR/skills" "$GEMINI_SKILLS_PATH"
ln -s "$REPO_DIR/agents" "$GEMINI_AGENTS_PATH"

# Symlink Claude
for path in "$CLAUDE_SKILLS_PATH" "$CLAUDE_CODE_SKILLS_PATH" "$AGENTS_SKILLS_PATH"; do
    mkdir -p "$(dirname "$path")"
    rm -rf "$path"
    ln -s "$REPO_DIR/skills" "$path"
done

echo "ai-skills installation complete. Symlinks created for Gemini and Claude."
