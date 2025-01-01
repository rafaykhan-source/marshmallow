FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
RUN mkdir build
COPY . .

RUN uv venv

RUN uv pip install -e .

CMD [ "uv", "run", "src/marshmallow" ]
