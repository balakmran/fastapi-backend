import re
import subprocess
import sys
from pathlib import Path


def tag_release():
    """Create and push a git tag for the current version."""
    # Read current version from app/__init__.py
    init_path = Path("app/__init__.py")
    content = init_path.read_text()
    match = re.search(r'__version__ = "(\d+\.\d+\.\d+)"', content)

    if not match:
        print("Error: Could not find version in app/__init__.py")
        sys.exit(1)

    assert match is not None

    version = match.group(1)
    tag_name = f"v{version}"

    # Check if tag already exists
    try:
        existing_tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
        if tag_name in existing_tags:
            print(f"Tag {tag_name} already exists.")
            sys.exit(0)
    except subprocess.CalledProcessError:
        print("Error: Failed to list git tags.")
        sys.exit(1)

    print(f"Creating tag {tag_name}...")

    try:
        subprocess.run(["git", "tag", tag_name], check=True)
        print(f"Successfully created tag {tag_name}")

        print("Pushing tag to origin...")
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        print(f"Successfully pushed tag {tag_name}")

    except subprocess.CalledProcessError as e:
        print(f"Error creating/pushing tag: {e}")
        sys.exit(1)


if __name__ == "__main__":
    tag_release()
