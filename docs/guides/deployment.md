# Deployment & Workflow

This guide covers how to deploy the application and manage the release lifecycle.

## 🐳 Docker Deployment

The project includes a production-ready `Dockerfile`.

### Local Docker Run

You can run the entire stack (Application + Database) using Docker Compose:

```bash
just up
```

To stop and remove containers:

```bash
just down
```

### Production Build

To build the image manually for production:

```bash
docker build -t fastapi-backend .
```

## 🧪 Quality Assurance

We use a comprehensive suite of tools to ensure code quality.

### Running Checks

Run **all** quality checks (formatting, linting, type checking, tests) with one command:

```bash
just check
```

- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: `ty` (Static type checker)
- **Testing**: [Pytest](https://docs.pytest.org/)

## 🚀 Release Process

We follow [Semantic Versioning](https://semver.org/). Releases are automated using `just`.

### 1. Bump Version

Increment the version number in `pyproject.toml` and `app/__init__.py`.

```bash
# For a patch release (e.g., 0.1.0 -> 0.1.1)
just bump part="patch"

# For a minor release (e.g., 0.1.0 -> 0.2.0)
just bump part="minor"

# For a major release (e.g., 0.1.0 -> 1.0.0)
just bump part="major"
```

### 2. Create Release Tag

After merging the version bump to `main`, create and push a git tag. This will trigger the GitHub Release workflow.

```bash
just tag
```

> **Note**: Always update `CHANGELOG.md` with the new version details before bumping the version!
