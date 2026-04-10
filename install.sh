#!/usr/bin/env bash

# ai-skills/install.sh - Symlink Gemini and Claude skills/agents/commands

set -e

REPO_DIR=$(cd "$(dirname "$0")" && pwd)
SKILLS_DIR="$REPO_DIR/skills"
AGENTS_DIR="$REPO_DIR/agents"
COMMANDS_DIR="$REPO_DIR/commands"
BACKUP_DIR="$HOME/.ai-skills.backup.$(date +%Y%m%d_%H%M%S)"

# Target directories to symlink
# Format: <target_path> <type: skills|agents|commands>
TARGETS=(
    "$HOME/.gemini/skills skills"
    "$HOME/.gemini/agents agents"
    "$HOME/.gemini/commands commands"
    "$HOME/.claude/skills skills"
    "$HOME/.claude/agents agents"
    "$HOME/.claude/commands commands"
)

# Legacy paths to consolidate/backup
LEGACY_PATHS=(
    "$HOME/.claude-code/skills"
    "$HOME/.agents/skills"
)

echo "Starting ai-skills installation..."

mkdir -p "$BACKUP_DIR"

# 1. Backup and Consolidate Legacy Paths
for path in "${LEGACY_PATHS[@]}"; do
    if [ -d "$path" ] && [ ! -L "$path" ]; then
        echo "Backing up and consolidating legacy path: $path"
        backup_path="$BACKUP_DIR/legacy_$(basename "${path//\//_}")"
        mkdir -p "$backup_path"
        cp -rp "$path"/. "$backup_path/" 2>/dev/null || true
        
        # Merge content into repo
        echo "Merging $path into $SKILLS_DIR..."
        cp -rp "$path"/. "$SKILLS_DIR/" 2>/dev/null || true
        
        rm -rf "$path"
    elif [ -L "$path" ]; then
        echo "Removing legacy symlink: $path"
        rm "$path"
    fi
done

# 2. Setup Symlinks and Backup Existing Data
for item in "${TARGETS[@]}"; do
    read -r target type <<< "$item"
    target_dir=$(dirname "$target")
    repo_source="$REPO_DIR/$type"
    
    mkdir -p "$target_dir"
    
    if [ -d "$target" ] && [ ! -L "$target" ]; then
        echo "Backing up existing directory: $target"
        backup_path="$BACKUP_DIR/$(basename "${target//\//_}")"
        mkdir -p "$backup_path"
        cp -rp "$target"/. "$backup_path/" 2>/dev/null || true
        
        # Copy user content to the repo directory BEFORE symlinking
        echo "Merging $target into $repo_source..."
        cp -rp "$target"/. "$repo_source/" 2>/dev/null || true
        
        rm -rf "$target"
    elif [ -L "$target" ]; then
        echo "Updating existing symlink: $target"
        rm "$target"
    fi

    echo "Creating symlink: $target -> $repo_source"
    ln -s "$repo_source" "$target"
done

# Clean up empty backup dir if nothing was backed up
if [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
    rmdir "$BACKUP_DIR"
else
    echo "Backups created in: $BACKUP_DIR"
fi

echo "ai-skills installation complete."
