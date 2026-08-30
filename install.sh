#!/usr/bin/env bash

# ai-skills/install.sh - Symlink Claude skills/agents/commands/rules

set -e

REPO_DIR=$(cd "$(dirname "$0")" && pwd)
SKILLS_DIR="$REPO_DIR/skills"
AGENTS_DIR="$REPO_DIR/agents"
COMMANDS_DIR="$REPO_DIR/commands"
BACKUP_DIR="$HOME/.ai-skills.backup.$(date +%Y%m%d_%H%M%S)"

# Target directories to symlink
# Format: <target_path> <type: skills|agents|commands|plugin>
TARGETS=(
    "$HOME/.claude/skills skills"
    "$HOME/.claude/agents agents"
    "$HOME/.claude/commands commands"
    "$HOME/.claude/CLAUDE.md rules/CLAUDE.md"
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

    if [[ "$type" != *.* ]] && [ ! -d "$repo_source" ]; then
        mkdir -p "$repo_source"
    fi

    if [ ! -d "$target_dir" ]; then
        mkdir -p "$target_dir"
    fi

    if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "Backing up existing path: $target"
        backup_path="$BACKUP_DIR/$(basename "${target//\//_}")"
        if [ -d "$target" ]; then
            mkdir -p "$backup_path"
            cp -rp "$target"/. "$backup_path/" 2>/dev/null || true

            # Copy user content to the repo directory BEFORE symlinking
            echo "Merging directory $target into $repo_source..."
            cp -rp "$target"/. "$repo_source/" 2>/dev/null || true
        else
            cp -p "$target" "$backup_path" 2>/dev/null || true

            # Copy user content to the repo directory BEFORE symlinking
            echo "Merging file $target into $repo_source..."
            cp -p "$target" "$repo_source" 2>/dev/null || true
        fi

        rm -rf "$target"
    elif [ -L "$target" ]; then
        echo "Updating existing symlink: $target"
        rm "$target"
    fi

    echo "Creating symlink: $target -> $repo_source"
    ln -s "$repo_source" "$target"
done

# 3. Setup Claude Code Plugin Marketplace
if command -v claude >/dev/null 2>&1 && [ -f "$REPO_DIR/.claude-plugin/marketplace.json" ]; then
    echo "Registering ai-skills as a Claude Code marketplace..."
    claude plugin marketplace add "$REPO_DIR" >/dev/null 2>&1 || claude plugin marketplace update ai-skills >/dev/null 2>&1

    for plugin_dir in "$REPO_DIR"/plugins/*; do
        if [ -d "$plugin_dir" ]; then
            plugin_name=$(basename "$plugin_dir")
            echo "Installing Claude Code plugin: $plugin_name@ai-skills"
            claude plugin install "$plugin_name@ai-skills" >/dev/null 2>&1
        fi
    done
else
    echo "Skipping Claude Code plugin marketplace setup (claude CLI not found or marketplace.json missing)."
fi

# 3b. Configure Statusline
STATUSLINE_SRC="$REPO_DIR/scripts/statusline.py"
SETTINGS_FILE="$HOME/.claude/settings.json"
statusline_ok=0

if [ -f "$STATUSLINE_SRC" ]; then
    chmod +x "$STATUSLINE_SRC"

    if command -v python3 >/dev/null 2>&1; then
        if python3 - "$SETTINGS_FILE" "$STATUSLINE_SRC" <<'PYEOF'
import json
import os
import sys

settings_path, command = sys.argv[1], sys.argv[2]
settings = {}

if os.path.exists(settings_path):
    try:
        with open(settings_path, encoding="utf-8") as fh:
            settings = json.load(fh) or {}
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"Could not parse {settings_path}: {exc}\n")
        sys.exit(1)
    if not isinstance(settings, dict):
        sys.stderr.write(f"{settings_path} is not a JSON object; leaving it alone.\n")
        sys.exit(1)

settings["statusLine"] = {"type": "command", "command": command, "padding": 0}

os.makedirs(os.path.dirname(settings_path), exist_ok=True)
tmp_path = f"{settings_path}.tmp"
with open(tmp_path, "w", encoding="utf-8") as fh:
    json.dump(settings, fh, indent=2)
    fh.write("\n")
os.replace(tmp_path, settings_path)
PYEOF
        then
            echo "Statusline configured: $STATUSLINE_SRC"
            statusline_ok=1
        else
            echo "Warning: could not update statusLine in $SETTINGS_FILE. Add it manually:"
            echo "  \"statusLine\": {\"type\": \"command\", \"command\": \"$STATUSLINE_SRC\", \"padding\": 0}"
        fi
    else
        echo "Skipping statusline setup (python3 not found)."
    fi
else
    echo "Skipping statusline setup ($STATUSLINE_SRC missing)."
fi

# Clean up empty backup dir if nothing was backed up
if [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
    rmdir "$BACKUP_DIR"
else
    echo "Backups created in: $BACKUP_DIR"
fi

# 4. Verification Checks
echo "Verifying installation..."
errors=0

# Verify TARGETS symlinks
for item in "${TARGETS[@]}"; do
    read -r target type <<< "$item"
    if [ ! -L "$target" ]; then
        echo "Error: Symlink target does not exist or is not a symlink: $target"
        errors=$((errors + 1))
    elif [ ! -e "$target" ]; then
        echo "Error: Broken symlink at: $target -> $(readlink "$target")"
        errors=$((errors + 1))
    else
        echo "Valid: $target -> $(readlink "$target")"
    fi
done

# Verify statusline wiring
if [ "$statusline_ok" -eq 1 ]; then
    if [ -x "$STATUSLINE_SRC" ]; then
        echo "Valid: statusLine -> $STATUSLINE_SRC"
    else
        echo "Error: statusline script is not executable: $STATUSLINE_SRC"
        errors=$((errors + 1))
    fi
fi

if [ $errors -eq 0 ]; then
    echo "--------------------------------------------------"
    echo "SUCCESS: All verification checks passed!"
    echo "--------------------------------------------------"
    echo "ai-skills installation complete."
else
    echo "--------------------------------------------------"
    echo "FAILURE: $errors installation verification error(s) found!"
    echo "--------------------------------------------------"
    exit 1
fi
