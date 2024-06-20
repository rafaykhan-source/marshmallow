# Marshmallow Bot!

Automates administrative and managerial tasks on Princeton EBCAO Discords.

## Configuration:

In the `marshmallow` directory:

`./scripts/setup.sh`

Create the virtual environment:

`python3 -m venv ~/.virtualenvs/marshmallow && source ~/.virtualenvs/marshmallow/bin/activate`

`pip install . && pip install .[development]`

## Start Up (Docker Compose):

`docker-compose up --build -d --force-recreate`

## Start Up (Docker):

`docker build -t marshmallow-main:latest .`

`docker container run --rm --detach --name marsh marshmallow-main`

## Acknowledgements

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)