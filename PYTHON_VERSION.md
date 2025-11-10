# Python Version Standard

## 🎯 Required Python Version

**All Gravity MicroServices MUST use Python 3.12.10**

## Why Python 3.12.10?

1. **Stability** - Production-ready stable release
2. **Performance** - Significant performance improvements over 3.11
3. **Type Hints** - Enhanced type system with PEP 695, 698
4. **Error Messages** - Better error messages and debugging
5. **Standard Library** - Improved asyncio, pathlib, and more
6. **Security** - Latest security patches

## Installation

### Windows

```powershell
# Download Python 3.12.10
# https://www.python.org/downloads/release/python-31210/

# Verify installation
python --version
# Should output: Python 3.12.10
```

### Linux/Ubuntu

```bash
# Using pyenv (recommended)
pyenv install 3.12.10
pyenv local 3.12.10

# Verify
python --version
```

### macOS

```bash
# Using pyenv (recommended)
brew install pyenv
pyenv install 3.12.10
pyenv local 3.12.10

# Verify
python --version
```

## Project Configuration

### pyproject.toml

All services must have:

```toml
[tool.poetry.dependencies]
python = "~3.12.10"  # Exact version requirement
```

### .python-version

Create `.python-version` file in each service root:

```
3.12.10
```

### Dockerfile

```dockerfile
FROM python:3.12.10-slim

# Your service setup...
```

## Verification

Check Python version in your service:

```bash
cd your-service/
python --version
# Must output: Python 3.12.10
```

## Services Using Python 3.12.10

✅ **Auth Service** - Python 3.12.10
✅ **User Service** - Python 3.12.10
✅ **Notification Service** - Python 3.12.10
⏳ **API Gateway** - Python 3.12.10
⏳ **Service Discovery** - Python 3.12.10

## Common Issues

### Wrong Python Version

```bash
# Error: Your Python version is 3.13.x
# Solution: Install Python 3.12.10

# Using pyenv
pyenv install 3.12.10
pyenv local 3.12.10
```

### Poetry Cache Issues

```bash
# Clear Poetry cache
poetry env remove python
poetry env use 3.12.10
poetry install
```

### Virtual Environment

```bash
# Create venv with specific Python
python3.12 -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate   # Windows

# Verify
python --version
```

## CI/CD Configuration

### GitHub Actions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12.10'
```

### Docker Compose

```yaml
services:
  your-service:
    image: python:3.12.10-slim
    # ...
```

## Migration Guide

If you have a service with different Python version:

1. **Update pyproject.toml**
   ```toml
   python = "~3.12.10"
   ```

2. **Create .python-version**
   ```bash
   echo "3.12.10" > .python-version
   ```

3. **Recreate environment**
   ```bash
   poetry env remove python
   poetry env use 3.12.10
   poetry install
   ```

4. **Test everything**
   ```bash
   pytest
   ```

5. **Update Dockerfile**
   ```dockerfile
   FROM python:3.12.10-slim
   ```

## Enforcement

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-python-version
        name: Check Python Version
        entry: python --version
        language: system
        pass_filenames: false
```

### Runtime Check

Add to `app/config.py`:

```python
import sys

REQUIRED_PYTHON = (3, 12, 10)

if sys.version_info[:3] != REQUIRED_PYTHON:
    raise RuntimeError(
        f"Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}.{REQUIRED_PYTHON[2]} is required. "
        f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
```

## Support

For Python version issues:
- Check official docs: https://www.python.org/downloads/release/python-31210/
- Team discussion: Use #tech-support channel
- Update this document: Submit PR with improvements

## References

- [Python 3.12 What's New](https://docs.python.org/3.12/whatsnew/3.12.html)
- [Python 3.12.10 Release Notes](https://www.python.org/downloads/release/python-31210/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 698 - Override Decorator](https://peps.python.org/pep-0698/)

---

**Last Updated:** 2025-11-09
**Mandatory for:** All Gravity MicroServices
**No Exceptions:** Python 3.12.10 is the standard
