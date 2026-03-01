#!/bin/bash

# Auto-push script for Obsidian documents
# Checks for changes and pushes to GitHub if any exist

cd /home/admin/doc

# Check if there are any changes
git add -A
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    echo "No changes to commit."
    exit 0
fi

echo "Changes detected:"
echo "$CHANGES"
echo ""

# Commit changes
git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to GitHub
git push origin main

if [ $? -eq 0 ]; then
    echo "Successfully pushed changes to GitHub."
else
    echo "Failed to push changes."
    exit 1
fi
