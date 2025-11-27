
# Justfile for FastAPI Backend

set dotenv-load

# Install all dependencies
install:
    uv sync --all-groups

# Clean build artifacts and cache
clean:
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @find . -type f -name "*.pyc" -delete 2>/dev/null || true
    @find . -type f -name "*.pyo" -delete 2>/dev/null || true
    @find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name "site" -exec rm -rf {} + 2>/dev/null || true
    @echo "✨ Clean complete!"

# Start Docker containers (all services)
up:
    VERSION=$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml) docker compose up -d --build

# Start only the database container
db:
    docker compose up -d db

# Stop Docker containers
down:
    docker compose down

# Run local development server
run:
    uv run fastapi dev app/main.py

# Run linting
lint:
    @uv run ruff check . --fix

# Run formatting
format:
    @uv run ruff format .

# Run type checking
typecheck:
    @uv run ty check

# Run tests with coverage
test:
	@uv run pytest -q --cov=app --cov-report=html --cov-report=term:skip-covered --tb=line tests/

# Run all quality checks
check:
    @echo ""
    @echo "🔧 Running formatter..."
    @echo "═════════════════════════════"
    @just format
    @echo ""
    @echo "✨ Running linter..."
    @echo "═════════════════════════════"
    @just lint
    @echo ""
    @echo "🔍 Running type checker..."
    @echo "═════════════════════════════"
    @just typecheck
    @echo ""
    @echo "🧪 Running tests..."
    @echo "═════════════════════════════"
    @just test
    @echo ""
    @echo "✅ All checks passed!"
    @echo ""

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Build documentation
docs-build:
    uv run mkdocs build

# Serve documentation locally
docs-serve:
    uv run mkdocs serve -a localhost:8001

# Generate a new migration
migrate-gen message:
    uv run alembic revision --autogenerate -m "{{message}}"

# Apply migrations
migrate-up:
    uv run alembic upgrade head
