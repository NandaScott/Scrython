#!/usr/bin/env python3
"""Update version in pyproject.toml with git commit hash for TestPyPI uploads."""

import re
import subprocess
import sys
from pathlib import Path


def get_git_commit_hash() -> str:
    """Get the short git commit hash (7 characters)."""
    result = subprocess.run(
        ["git", "rev-parse", "--short=7", "HEAD"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def update_version_in_pyproject() -> str:
    """Add git commit hash to version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("ERROR: pyproject.toml not found in current directory")
        sys.exit(1)

    content = pyproject_path.read_text()

    # Find current version
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not version_match:
        print("ERROR: Could not find version in pyproject.toml")
        sys.exit(1)

    current_version = version_match.group(1)
    commit_hash = get_git_commit_hash()

    # Create new version with PEP 440 local identifier
    new_version = f"{current_version}+{commit_hash}"

    # Replace version in content
    new_content = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    # Write back (temporary, only in workflow workspace)
    pyproject_path.write_text(new_content)

    print(f"Version updated: {current_version} -> {new_version}")
    return new_version


if __name__ == "__main__":
    try:
        version = update_version_in_pyproject()
        # Output for GitHub Actions
        print(f"::set-output name=version::{version}")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
