# Quality Checks

This guide covers the quality assurance tools and workflows to ensure code quality before committing changes.

---

## Overview

The project uses a comprehensive suite of automated tools to maintain code quality:

- **Formatting**: [Ruff](https://github.com/astral-sh/ruff) formatter
- **Linting**: [Ruff](https://github.com/astral-sh/ruff) linter
- **Type Checking**: `ty` static type checker
- **Testing**: [Pytest](https://docs.pytest.org/) with coverage

---

## Running All Checks

Run **all** quality checks with a single command:

```bash
just check
```

This command runs all checks in sequence:

1. **Format** → Auto-fixes code style
2. **Lint** → Checks for code issues
3. **Typecheck** → Verifies type annotations
4. **Test** → Runs test suite with coverage

If all checks pass, you'll see:

```
All checks passed!
```

---

## Individual Checks

### Format Code

```bash
just format
```

Automatically formats all Python files using Ruff.

**What it fixes**:

- Line length (max 80 characters)
- Import ordering
- Trailing whitespace
- Quote normalization

### Lint Code

```bash
just lint
```

Checks for code quality issues without modifying files.

**What it checks**:

- Unused imports
- Undefined variables
- Style violations
- Complexity issues

### Type Check

```bash
just typecheck
```

Validates all type annotations using `ty`.

**Requirements**:

- 100% type hint coverage
- No type errors
- Proper return types

### Run Tests

```bash
just test
```

Runs the full test suite with coverage reporting.

**Requirements**:

- All tests pass
- Coverage = 100% (enforced; the run fails below it)

---

## Git Hooks

One command installs both hooks (`just setup` does it too, for new
clones):

```bash
just pi  # Install pre-commit + pre-push hooks
```

They run at two different points, with deliberately different scope:

| Hook           | Runs                                  | Why there                                  |
| :------------- | :------------------------------------ | :----------------------------------------- |
| **pre-commit** | ruff format, ruff check, `ty`         | Fast enough to sit in every commit          |
| **pre-push**   | the full pytest suite                 | Too slow per commit; catches breakage pre-remote |

```bash
git commit -m "feat: add new feature"
# → Runs format, lint, typecheck on changed files

git push
# → Runs the full test suite
```

!!! warning "The pre-push hook needs Postgres"

    The suite runs against a real database, so start it first with
    `just db` or the push aborts. `just test` and `just check`
    auto-start it; the git hook does not.

`git push --no-verify` skips the gate. Use it only in emergencies — it
exists to stop broken code reaching the remote.

To run the pre-commit hooks manually across all files:

```bash
just pr  # Run pre-commit hooks on all files
```

---

## CI Integration

All quality checks run automatically on every push via GitHub Actions,
across a Python 3.12 / 3.13 / 3.14 matrix:

```yaml
# .github/workflows/ci.yml
- name: Run quality checks
  run: just check
```

That one step covers everything, coverage included — the threshold is
enforced by `fail_under` in `[tool.coverage.report]`
([`pyproject.toml`](../../pyproject.toml)), not by a separate CI step,
so the same gate applies locally and in CI.

Dependency CVE scanning is **not** part of this pipeline or of
`just check` — it needs network access and its result depends on the
OSV database rather than on your code. Run `just audit` by hand after
dependency changes; see
[Dependency Scanning](dependency-scanning.md#uv-audit).

Pull requests cannot be merged until all checks pass ✅

---

## Quality Standards

The project maintains strict quality standards:

| Check           | Requirement    | Tool   |
| --------------- | -------------- | ------ |
| **Formatting**  | 100% compliant | Ruff   |
| **Linting**     | 0 violations   | Ruff   |
| **Type Hints**  | 100% coverage  | ty     |
| **Tests**       | 100% coverage  | Pytest |
| **Line Length** | ≤80 chars      | Ruff   |

---

## Quick Reference

| Task           | Command          |
| -------------- | ---------------- |
| Run all checks | `just check`     |
| Format code    | `just format`    |
| Lint code      | `just lint`      |
| Type check     | `just typecheck` |
| Run tests      | `just test`      |
| Install hooks  | `just pi`        |
| Run hooks      | `just pr`        |
| Audit deps for CVEs | `just audit` |
| Sync `main` after a merge | `just sync-main` |

---

## Troubleshooting

### Format Conflicts

If Ruff format changes conflict with manual edits:

```bash
# Reformat everything
just format
```

### Type Errors

If type checking fails:

1. Check return types include `| None` where needed
2. Add type parameters to generics: `list[User]`
3. Use `from __future__ import annotations` for forward refs

### Coverage Below Threshold

`just check` fails with `Required test coverage of 100.0% not reached`
when any line or branch goes uncovered. The terminal report lists the
gaps under `Missing`; for a browsable view:

```bash
# Generate HTML coverage report
just test
open htmlcov/index.html
```

Find untested lines and add tests. If a line genuinely cannot be
covered, mark it `# pragma: no cover` rather than lowering the gate.

---

## See Also

- [Testing Guide](testing.md) — Writing and running tests
- [Troubleshooting](troubleshooting.md) — Common quality check issues
- [Contributing Guide](../project/contributing.md) — Development workflow
