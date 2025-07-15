# Marshmallow

Automates administrative and managerial tasks on Princeton EBCAO Discords.

## Development Setup

The project uses `ruff`, `mypy`, and `pre-commit` for linting, formatting,
type-checking, and code consistency checks. You can install all of
these tools using `uv tool install` and run them on the project
where the respective tool configurations are stored in the
`pyproject.toml`.

Setup the virtual environment:

```bash
uv venv
```

Setup pre-commit:

```bash
pre-commit autoupdate
pre-commit install
pre-commit run -a
```

In the root directory, run:

```bash
mkdir build logs data assignments messages
```

## Usage (Local)

```bash
uv run src/marshmallow
```

## Usage (Docker Compose)

```bash
docker compose up --build -d --force-recreate
```

## Usage (Docker)

```bash
docker build -t marshmallow-main:latest .
docker container run --rm --detach --name marsh marshmallow-main
```

## Marshmallow Operations (Archive)

1. /info member

Developed to quickly retrieve username, nickname, display name, and roles.

> [!NOTE]
> It helps diagnose whether discord.py is properly detecting members’ various aliases, which is integral for the bot's name-matching algorithm.

2. /clone_role role new_role_name

Instead of creating a new role and tediously updating permissions, clone an existing role with similar or the same permissions and modify accordingly.

> [!NOTE]
> Discord does not have a UI method for duplicating roles, so this command was implemented.

3. /peep

This is a marshmallow thematic rendition of the idiomatic /ping command to check whether the bot is responding.

4. /about

This is just for the curious.

5. /sync

Updates Marshmallow’s registered slash commands and documentation.

6. /*load cog_name

This allows bot code to be dynamically updated, added, or removed without taking down the bot.

7. /clone_roles role base_name start end

Make Zee Group 9 to 14 (inclusive) Roles.

8. /clone_roles channel base_name start end

Make zee-group-9 to 14 (inclusive) channels.

9. /delete_roles base_name

Remove all roles with “Spring Mentorship” in its name.

11. /count_daily_activity channel

Marks daily activity of each person in the channel, producing a csv.

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
