import re
import sys
from pathlib import Path


def bump_version(part: str):
    """Bump the version in pyproject.toml and app/__init__.py.

    Args:
        part: The part of the version to increment (major, minor, patch).
    """
    pyproject_path = Path("pyproject.toml")
    init_path = Path("app/__init__.py")

    # Read current version from pyproject.toml
    content = pyproject_path.read_text()
    match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)

    # Assert match is not None for type checker
    assert match is not None

    major, minor, patch = map(int, match.groups())

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Error: Invalid part '{part}'. Use major, minor, or patch.")
        sys.exit(1)

    new_version = f"{major}.{minor}.{patch}"

    # Update pyproject.toml
    new_content = re.sub(
        r'version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        content,
        count=1,
    )
    pyproject_path.write_text(new_content)

    # Update app/__init__.py
    init_content = init_path.read_text()
    new_init_content = re.sub(
        r'__version__ = ".*"', f'__version__ = "{new_version}"', init_content
    )
    init_path.write_text(new_init_content)

    print(f"Bumped version to {new_version}")


if __name__ == "__main__":
    EXPECTED_ARGS = 2
    if len(sys.argv) != EXPECTED_ARGS:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)

    bump_version(sys.argv[1])
