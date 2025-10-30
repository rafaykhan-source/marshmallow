FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY . .

RUN uv venv && uv pip install -e .

CMD [ "uv", "run", "src/marshmallow" ]
