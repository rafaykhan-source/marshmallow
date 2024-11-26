# Marshmallow Bot!

Automates administrative and managerial tasks on Princeton EBCAO Discords.

## Configuration:

### Development Setup

In the `marshmallow` directory, run:
```bash
mkdir build logs data assignments messages
pre-commit install
```

## Usage (Local):
```bash
uv run src/marshmallow/run.py
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