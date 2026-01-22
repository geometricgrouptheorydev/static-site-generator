#!/bin/bash

if [ "$1" == "github" ]; then
    # Auto-detect repo name for GitHub Pages
    REPO_NAME=$(git remote get-url origin | sed 's/.*\/\([^/]*\)\.git/\1/' | sed 's/.*\/\([^/]*\)$/\1/')
    BASEPATH="/$REPO_NAME/"
else
    # Custom domain or explicit path
    BASEPATH="${1:-/}"
fi

echo "Building with basepath: $BASEPATH"
python3 src/main.py "$BASEPATH"