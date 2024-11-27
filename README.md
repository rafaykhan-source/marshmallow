# Marshmallow Bot!

Automates administrative and managerial tasks on Princeton EBCAO Discords.

## Development Setup
The project uses `ruff`, `mypy`, and `pre-commit` for linting, formatting, type-checking, and code consistency checks. You can install all of these tools using `uv tool install` and run them on the project where the respective tool configurations are stored in the `pyproject.toml`.

Setup the virtual environment:
```
uv venv
```

Setup pre-commit:
```
pre-commit autoupdate
pre-commit install
pre-commit run -a
```

In the root directory, run:
```bash
mkdir build logs data assignments messages
```

## Usage (Local):
```bash
uv run src/marshmallow
```

## Usage (Docker Compose):

```bash
docker compose up --build -d --force-recreate
```

## Usage (Docker):

```bash
docker build -t marshmallow-main:latest .
docker container run --rm --detach --name marsh marshmallow-main
```

## Acknowledgements

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)