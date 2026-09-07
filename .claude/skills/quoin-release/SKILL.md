---
name: quoin-release
description: Use this skill whenever the user wants to cut a release, ship a version, bump the version, tag a release, publish a new version, prepare a changelog entry, or do anything that ends with a `vX.Y.Z` git tag on this QuoinAPI project. Triggers include phrases like "release 0.7.0", "cut a patch release", "ship a new version", "bump the minor version", "tag the release", "prepare the changelog for release", or "let's release". Do NOT use for: editing the changelog mid-development without releasing, hotfix/emergency-patch releases (that is `quoin-hotfix`), or generating release notes for an already-tagged version.
allowed-tools: Read, Edit, Bash
model: haiku
---

# Releasing QuoinAPI

A QuoinAPI release is a small, ordered ritual: changelog → version bump → changelog rename → commit → merge → tag → publish. The tag does **not** publish anything by itself — no release workflow exists in this repo, so the last step is yours to run. The long-form rationale lives in [docs/guides/release-workflow.md](../../../docs/guides/release-workflow.md); this skill is the in-the-moment checklist.

## Before you start

Confirm three things with the user (or from the repo state) before touching anything:

1. **Bump type** — `patch` (bug fixes), `minor` (new features, backwards-compatible), `major` (breaking). SemVer rules apply.
2. **Branch** — you should be on a clean working branch off `main`, not on `main` directly. The changelog/version commit goes through PR review like any other change.
3. **What's actually shipping** — skim `git log <last-tag>..HEAD` so the changelog reflects reality. The `[Unreleased]` section is often stale or incomplete.

Then run `just audit` — CVE scanning is not in CI, so a release is the
last checkpoint before shipping vulnerable dependencies. Remediation
ladder in [docs/guides/dependency-scanning.md](../../../docs/guides/dependency-scanning.md).

## Workflow

### 1. Curate the `[Unreleased]` section in `CHANGELOG.md`

Open `CHANGELOG.md`. The top-most section is `## [Unreleased]`. Make sure it accurately captures everything merged since the last tag.

**Section order within a release** (omit any that are empty):

1. Added
2. Changed
3. Deprecated
4. Removed
5. Fixed
6. Security

This order is non-negotiable — it matches Keep a Changelog and the project's prior releases. Don't invent new section names.

Each entry is a bullet describing user-visible impact, not the diff. Group related bullets under a bold sub-label when it helps scanning (see prior releases for the `**Security**:`, `**Developer Experience**:` style).

### 2. Bump the version

```bash
just bump part="patch"   # or minor, or major
```

This updates the version string in **both** `pyproject.toml` and `app/__init__.py` via `scripts/bump_version.py`. It does not touch the changelog or git.

After running, note the new version — you'll use it in the next two steps.

### 3. Promote `[Unreleased]` to the new version in `CHANGELOG.md`

Rename the heading from `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` using today's date, and insert a fresh empty `## [Unreleased]` section above it so the next cycle has somewhere to land entries.

Example transition:

```markdown
## [Unreleased]

## [0.7.0] - 2026-04-25

### Added
- ...
```

### 4. Commit and merge

```bash
git add CHANGELOG.md pyproject.toml app/__init__.py
git commit -m "docs: update changelog for vX.Y.Z"
```

Push the branch and merge the PR to `main` the normal way. **Do not tag from a feature branch** — the tag must point at the merge commit on `main` so the release reflects what's actually shipped.

### 5. Tag the release

Once the changelog/bump commit is on `main` and you've pulled it locally:

```bash
just tag
```

`scripts/tag_release.py` reads the version from `app/__init__.py`, creates `vX.Y.Z`, and pushes it to `origin`. The script refuses to re-create an existing tag, so it's safe to re-run.

The tag push does **not** publish a GitHub Release. `copier-update.yml` is the
only tag-triggered workflow in this repo; it verifies the `copier update` path
and nothing else. Continue to step 6.

### 6. Publish the GitHub Release

Create it explicitly, using that version's changelog section as the body:

```bash
awk '/^## \[X\.Y\.Z\]/{f=1;next} /^## \[/{f=0} f' CHANGELOG.md \
  | gh release create vX.Y.Z --title vX.Y.Z --verify-tag --notes-file -
```

The `awk` prints the section between this version's `## [X.Y.Z] - date`
heading and the next one, which is exactly the body shape `v0.8.0` through
`v0.11.0` use. `--verify-tag` aborts if step 5's tag never reached `origin`,
so a typo fails loudly instead of creating a release against a missing tag.

Match the existing releases: the title is the bare tag (`v0.11.0`, no prose),
neither draft nor pre-release. For a release candidate, add `--prerelease`.

## After the tag

Verify the release landed:

- Confirm the GitHub Release page shows the `vX.Y.Z` entry with the changelog body.
- Check the Actions tab: CI on `main` and **Copier Update Check** on the tag
  should both be green. The update check is the one that matters — it proves
  `copier update` still applies cleanly across the release boundary.
- Pull `main` and confirm `git describe --tags` reports the new tag.

If `gh release create` fails, **don't delete the tag** — fix the input and
re-run the command; the tag is already public and deleting it breaks anyone
who pulled it. If the *release* is wrong rather than the tag, edit it in place
with `gh release edit vX.Y.Z --notes-file -`.

## Things that bite

- **Forgetting to update the changelog before bumping** — the bump script doesn't check, and you'll end up with a `vX.Y.Z` tag whose changelog entry is empty or wrong. Always do step 1 first.
- **Tagging from the feature branch** — the tag will point at a commit that isn't on `main`, and the GitHub Release will reflect a tree no one else sees. Always merge first, pull `main`, then `just tag`.
- **Skipping a section out of section order** — if you add a `### Fixed` block above `### Added`, the reader's eye loses the convention. Reorder before committing.
- **Using `chore:` instead of `docs:` for the release commit** — convention here is `docs: update changelog for vX.Y.Z`. It keeps the release commits trivially greppable.

## When the user asks for "just bump the version"

If the user asks only to bump (not to release), do step 2 and stop — don't touch the changelog or push tags. A bare bump is sometimes useful mid-development to move a pre-release version forward; treat it as a different intent than a full release and confirm before going further.
