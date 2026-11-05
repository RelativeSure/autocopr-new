#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <copr webhook url> <github sha>"
    exit 1
fi

COPR_WEBHOOK=$1
GITHUB_SHA=$2

# Optionally respect a root-level exclude_files list when present.
# This is kept intentionally loose so the script still works on repos that
# do not have config.yaml in place.
if [ -f config.yaml ]; then
    excluded_files=$(awk '/^exclude_files:/{f=1;next} f && /^[[:space:]]*-/{gsub(/^[[:space:]]*-[[:space:]]*/,"",$0);print;next} f{exit}' config.yaml)
    if [ -n "$excluded_files" ]; then
        echo "Excluded from COPR builds (config.yaml exclude_files): $excluded_files"
    fi
else
    excluded_files=""
fi

files_changed=$(git diff-tree --no-commit-id --name-only -r "$GITHUB_SHA" | grep '\.spec$')
echo "Files changed: $files_changed"

for file in $files_changed; do
    echo "Processing file: $file"
    filename=$(basename "$file")

    if [ -n "$excluded_files" ] && grep -qxF "$filename" <<<"$excluded_files"; then
        echo "Skipping $filename: excluded via config.yaml exclude_files"
        continue
    fi

    filename_without_ext="${filename%.*}"
    echo "Sending COPR webhook for package $filename_without_ext"
    curl -X POST "$COPR_WEBHOOK/$filename_without_ext/"
done
