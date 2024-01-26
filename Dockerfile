FROM python:3.10

COPY pyproject.toml /app/
WORKDIR /app

RUN mkdir build
RUN pip install .

COPY . .

CMD [ "python", "src/bot/run.py" ]