#!/usr/bin/env python3
"""Verify that `copier update` applies cleanly across a template release.

QuoinAPI is a Copier template, and `copier update` is how a project
generated from it takes later template improvements. That path is easy to
silently break — nothing in the normal test suite exercises it, since it
only runs against a *generated* project, not this repository itself.

This script proves the mechanism still works between two tags: generate a
project from the older tag, commit it as its own git repo (required for
`copier update` to compute a diff), then update it to the newer tag and
check the result is clean.

By default it answers only "does `copier update` itself work" — no
conflicts, and the answers file records the new tag. Pass `--check` to
also run the *updated* project's own `just check`, which answers the
other half: that what an adopter is left holding after an update still
builds, types, migrates and passes its tests.

`--check` is opt-in because it needs a reachable Postgres and the
generated project's own settings prefix in the environment (`--defaults`
yields `QUOINAPI_*`). CI supplies both; a local run wanting the same
proof must too, and must not have its own stack already bound to the
port. `CI=true` is set for the gate so the project's `_db-check` skips
`docker compose` and uses whatever database the environment points at.

Usage:
    uv run python scripts/verify_template_update.py \
        <previous-tag> <current-tag> [--check]
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_COMMIT_LINE = re.compile(r"^_commit:\s*(\S+)\s*$", re.MULTILINE)
EXPECTED_TAG_ARGS = 2


def _run(
    args: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> None:
    """Run a subprocess, raising with combined output on failure.

    Args:
        args: The command and its arguments.
        cwd: Working directory to run the command in.
        env: Complete environment for the child. Replaces (does not
            merge with) the parent's — pass `{**os.environ, ...}` to
            extend it. Callers rely on this to isolate git from a
            developer's global config.

    Raises:
        SystemExit: If the command exits non-zero.
    """
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        print(f"[verify-template-update] command failed: {' '.join(args)}")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)


def _git_commit_all(repo: Path, message: str) -> None:
    """Init a git repo (if needed) and commit everything in it.

    `copier update` requires the destination to be a git repository so it
    can three-way-merge template changes against local evolution.
    """
    if not (repo / ".git").exists():
        _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    env = {
        "GIT_AUTHOR_NAME": "quoin-ci",
        "GIT_AUTHOR_EMAIL": "ci@quoin-api.invalid",
        "GIT_COMMITTER_NAME": "quoin-ci",
        "GIT_COMMITTER_EMAIL": "ci@quoin-api.invalid",
    }
    _run(["git", "add", "-A"], cwd=repo)
    _run(["git", "commit", "-q", "-m", message], cwd=repo, env=env)


def _check_no_conflicts(project: Path) -> None:
    """Fail if `copier update` left any `.rej` conflict files behind."""
    rejects = sorted(project.rglob("*.rej"))
    if not rejects:
        return
    print("[verify-template-update] copier update left conflict files:")
    for rej in rejects:
        print(f"\n--- {rej.relative_to(project)} ---")
        print(rej.read_text(errors="replace"))
    raise SystemExit(1)


def _check_recorded_commit(project: Path, expected_tag: str) -> None:
    """Fail unless `.copier-answers.yml` now records the expected tag."""
    answers_path = project / ".copier-answers.yml"
    if not answers_path.is_file():
        print(
            "[verify-template-update] .copier-answers.yml is missing "
            "after update"
        )
        raise SystemExit(1)
    match = _COMMIT_LINE.search(answers_path.read_text())
    recorded = match.group(1) if match else None
    if recorded != expected_tag:
        print(
            f"[verify-template-update] .copier-answers.yml records "
            f"'{recorded}', expected '{expected_tag}'"
        )
        raise SystemExit(1)


def _run_project_gate(project: Path) -> None:
    """Run the updated project's own `just check`.

    Args:
        project: The generated project, already updated to the new tag.
    """
    # Full environment: `just` needs PATH, and the project needs whatever
    # <PREFIX>_POSTGRES_* the caller set. CI=true makes its `_db-check`
    # skip `docker compose` and trust that database.
    env = {**os.environ, "CI": "true"}
    print("[verify-template-update] installing the updated project...")
    _run(["just", "install"], cwd=project, env=env)
    print("[verify-template-update] running the updated project's gate...")
    _run(["just", "check"], cwd=project, env=env)


def verify(
    previous_tag: str, current_tag: str, *, run_check: bool = False
) -> None:
    """Generate from `previous_tag`, update to `current_tag`, and verify.

    Args:
        previous_tag: The older template tag to generate a project from.
        current_tag: The newer template tag to update that project to.
        run_check: Also run the updated project's own `just check`.
    """
    with tempfile.TemporaryDirectory(prefix="quoin-template-update-") as tmp:
        project = Path(tmp) / "generated-project"

        print(f"[verify-template-update] generating from {previous_tag}...")
        _run(
            [
                "uvx",
                "copier",
                "copy",
                "--defaults",
                "--trust",
                "--vcs-ref",
                previous_tag,
                str(REPO_ROOT),
                str(project),
            ],
            cwd=REPO_ROOT,
        )
        _git_commit_all(project, "initial")

        print(f"[verify-template-update] updating to {current_tag}...")
        _run(
            [
                "uvx",
                "copier",
                "update",
                "--defaults",
                "--trust",
                # Force .rej conflict files. Copier's default `inline`
                # mode writes conflict markers into the files and deletes
                # the .rej witnesses, which `_check_no_conflicts` (a .rej
                # glob) would then miss — silently passing a conflicted
                # update.
                "--conflict",
                "rej",
                "--vcs-ref",
                current_tag,
            ],
            cwd=project,
        )

        _check_no_conflicts(project)
        _check_recorded_commit(project, current_tag)

        if run_check:
            _run_project_gate(project)

    print(
        f"[verify-template-update] OK: {previous_tag} -> {current_tag} "
        "applied cleanly."
    )


def main(argv: list[str]) -> int:
    """Entry point.

    Returns:
        0 on a clean update, non-zero if `copier` is missing or the
        update left conflicts or an unexpected recorded commit.
    """
    args = list(argv[1:])
    run_check = "--check" in args
    if run_check:
        args.remove("--check")

    if len(args) != EXPECTED_TAG_ARGS:
        print(
            "Usage: python scripts/verify_template_update.py "
            "<previous-tag> <current-tag> [--check]"
        )
        return 1
    if shutil.which("uvx") is None:
        print("[verify-template-update] 'uvx' not found on PATH.")
        return 1
    if run_check and shutil.which("just") is None:
        print("[verify-template-update] '--check' needs 'just' on PATH.")
        return 1

    verify(args[0], args[1], run_check=run_check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
