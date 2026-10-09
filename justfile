set shell := ["bash", "-euo", "pipefail", "-c"]

# Show available recipes
default:
    @just --list

# Create the Python environment from the committed lockfile
setup:
    uv sync --locked

# Show the active toolchain
doctor:
    mise --version
    hugo version
    python --version
    uv --version
    just --version
    age --version
    gh --version
    uv lock --check

# Serve locally, including drafts
dev:
    hugo server -D

# Build the canonical site
build:
    hugo --minify --panicOnWarning

# Build an isolated preview locally; no upload
preview:
    hugo --minify --panicOnWarning --config hugo.toml,config/preview.toml --baseURL https://leipt.com/leipt-preview/ --destination public-preview

# Auto-format and fix Python tooling
fmt:
    uv run --locked ruff format scripts tests
    uv run --locked ruff check --fix scripts tests

# Check Python tooling without changes
lint:
    uv run --locked ruff format --check scripts tests
    uv run --locked ruff check scripts tests

# Verify secrets never publish after failed decryption
test:
    uv run --locked python -m unittest discover -s tests

# Verify the canonical build's expected outputs
check-output:
    test -s public/index.html
    test -s public/sitemap.xml
    test -s public/index.xml
    test -s public/contact/index.html

# Local gate, also used by CI
check: lint test build check-output

alias ci := check

# Encrypt dotenv secrets from stdin; AGE_RECIPIENT is a public age recipient
secrets-encrypt:
    uv run --locked python scripts/secrets.py encrypt

# Decrypt in memory and publish to GitHub's onecom-preview environment
secrets-sync:
    uv run --locked python scripts/secrets.py sync

# List GitHub secret names, never values
secrets-list:
    gh secret list --repo frecke/leipt.com --env onecom-preview
