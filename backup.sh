#!/bin/bash

echo "Running backup tasks..."

# Backup Claude Code configuration
if [ -f "$HOME/.claude.json" ]; then
  echo "Backing up Claude Code configuration..."
  $HOME/Projects/dotfiles/backup-claude-config.sh
else
  echo "Claude Code configuration not found, skipping backup"
fi

echo "Backup tasks completed!"