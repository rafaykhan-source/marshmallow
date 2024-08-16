# Marshmallow Bot!

Automates administrative and managerial tasks on Princeton EBCAO Discords.

## Configuration:

### Development Setup

In the `marshmallow` directory, run:
```bash
./scripts/setup.sh
```

To setup the virtual environment, run:
```bash
python3 -m venv ~/.virtualenvs/marshmallow
source ~/.virtualenvs/marshmallow/bin/activate
pip install . && pip install .[development]
pre-commit install
```

## Usage (Docker Compose):

```bash
docker-compose up --build -d --force-recreate
```

## Usage (Docker):

```bash
docker build -t marshmallow-main:latest .
docker container run --rm --detach --name marsh marshmallow-main
```

## Acknowledgements

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)