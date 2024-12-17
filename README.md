# E-Lib

API for managing an online library system

## Requirements

- [Python 3.13+](https://www.python.org/downloads/).
- [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## General Workflow

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

You can install all the dependencies with:

```bash
uv sync
```

Then you can activate the virtual environment with:

```bash
source .venv/bin/activate
```

To run the application in your development environment, use the following command:

```bash
uv run uvicorn app.main:app --reload
# OR
uvicorn app.main:app --reload
```

Check style with [Ruff](https://docs.astral.sh/ruff/):

```bash
# Check the style
uvx ruff check

# Fix the issues
uvx ruff check --fix

# Format the code
uvx ruff format
```

To run the tests suite, use the following command:

```bash
uv run pytest
# OR
pytest
```
