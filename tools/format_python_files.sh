#!/bin/bash

# Function to check if a command is available
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if black is installed
if ! command_exists black; then
  echo "Installing black..."
  pip install black==23.7.0
fi

# Get the root directory of the project using git
project_dir=$(git rev-parse --show-toplevel)

if [ -z "$project_dir" ]; then
  echo "Error: Not a git repository or no git root found!"
  exit 1
fi

# Format all Python files in the project using black
echo "Formatting Python files using black..."
find "$project_dir" -name "*.py" -exec black {} +
echo "Formatting complete!"
