FROM python:3.11.4 AS base
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root
COPY . /app
FROM python:3.11.4-slim
WORKDIR /app
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY . /app
CMD ["poetry", "run", "python", "app.py"]
