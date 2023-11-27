# syntax=docker/dockerfile:1.6

ARG PYTHON_VERSION=3.11.0-slim-bullseye
ARG POETRY_VERSION=1.7.1

FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt install -y --no-install-recommends netcat \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-dev

EXPOSE 8000
WORKDIR /app

COPY . .

CMD [ "poetry", "run", "uvicorn", "--host=0.0.0.0", "app.main:app" ]
