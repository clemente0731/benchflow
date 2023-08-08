#!/bin/bash

set -x  # Enable verbose mode
set -e  # Exit on any error

# Get the root directory of the Git project
git_root=$(git rev-parse --show-toplevel)

if [[ -n "$git_root" ]]; then
    echo "Changing to Git project root directory..."
    cd "$git_root" || exit 1

    # Change to the "tests" directory and run unit tests
    cd tests
    echo "Running unit tests..."
    python -m pytest -vv xtest*.py

else
    echo "Not in a Git project."
fi
