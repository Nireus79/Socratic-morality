# Publishing socratic-morality to PyPI

This document outlines the steps to publish socratic-morality to PyPI.

## Prerequisites

- PyPI account: https://pypi.org/
- GitHub Actions secrets configured
- Version updated in `pyproject.toml`

## Publishing Steps

### 1. Local Testing

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI first
twine upload -r testpypi dist/*
```

### 2. GitHub Release

Create a GitHub release with a version tag:

```bash
git tag v1.0.0-alpha
git push origin v1.0.0-alpha
```

### 3. Automated PyPI Publishing

The GitHub Actions workflow in `.github/workflows/publish.yml` will:
1. Trigger on git tag push (v*)
2. Build the package
3. Check the distribution
4. Publish to PyPI

### 4. Verify Publication

Visit: https://pypi.org/project/socratic-morality/

### Configuration

#### PyPI Token

Add to GitHub Secrets:
- `PYPI_API_TOKEN`: PyPI API token from https://pypi.org/manage/account/

#### Build Files

The package is configured via:
- `pyproject.toml`: Package metadata and dependencies
- `MANIFEST.in`: Additional files to include

## Version Numbering

- **Alpha**: 1.0.0-alpha (current - Foundation phase)
- **Beta**: 1.0.0-beta (after Phase 2 - Ethical reasoning complete)
- **Release**: 1.0.0 (after Phase 3 - Enterprise features complete)

## Timeline

- Phase 1: v1.0.0-alpha (Current - Foundation)
- Phase 2: v1.0.0-beta (Ethical reasoning + adapters)
- Phase 3: v1.0.0 (Zero-trust + storage backends)

