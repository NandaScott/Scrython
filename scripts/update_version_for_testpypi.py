#!/usr/bin/env python3
"""Update version in pyproject.toml with dev identifier for TestPyPI uploads."""

import os
import re
import sys
from pathlib import Path


def get_unique_identifier() -> str:
    """Get a unique identifier for the dev version.

    Uses GitHub Actions run number if available, otherwise falls back to
    a timestamp. This ensures each upload has a unique, incrementing version.
    """
    # GitHub Actions provides a unique, incrementing run number
    run_number = os.environ.get("GITHUB_RUN_NUMBER")
    if run_number:
        return run_number

    # Fallback for local testing: use timestamp
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def update_version_in_pyproject() -> str:
    """Add dev identifier to version in pyproject.toml."""
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
    unique_id = get_unique_identifier()

    # Create new version with PEP 440 dev identifier (accepted by PyPI/TestPyPI)
    new_version = f"{current_version}.dev{unique_id}"

    # Replace version in content
    new_content = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
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
