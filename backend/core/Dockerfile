FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /market/backend/core

COPY ./pyproject.toml /market/backend/core/pyproject.toml

RUN apt update \
    && pip install poetry \
    && apt install -y vim \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /market/backend/core \
    && chdir /market/backend/core \
    && poetry config virtualenvs.create false \
    && poetry install --only main

WORKDIR /market/backend/core/src

COPY --chown=app:app . /market/backend/core/

EXPOSE 8000

USER app

CMD ["sh", "/market/backend/core/entrypoint.sh"]
