#!/bin/bash

# Check if git repo is clean
if ! git diff-index --quiet HEAD --; then
    echo "Git repository is not clean. Commit or stash changes before running this script."
    exit 1
fi

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "No version argument provided. Please provide 'patch', 'minor', or 'major'."
    exit 1
fi

# Check if --dry-run option is set
DRY_RUN=0
if [ "$2" == "--dry" ]; then
    DRY_RUN=1
fi

# Bump version
OUTPUT=$(hatch version $1 2>&1)
OLD_VERSION=$(echo $OUTPUT | awk '{print $2}')
NEW_VERSION=$(echo $OUTPUT | awk '{print $4}')


# If --dry-run option is set, print actions and exit
if [ $DRY_RUN -eq 1 ]; then
    echo "Would commit with message: Bump from $OLD_VERSION to $NEW_VERSION"
    echo "Would create tag: v$NEW_VERSION"
    echo "Would push to remote repository"
    echo "Would push tags to remote repository"
    git reset --hard HEAD
    git clean -fd
    exit 0
fi

# Commit changes
git commit -am "Bump from $OLD_VERSION to $NEW_VERSION"

# Create tag
git tag -a "v$NEW_VERSION" -m "version $NEW_VERSION"

# Push changes and tags
git push
git push --tags