FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /market/backend

COPY ./pyproject.toml /market/backend/pyproject.toml

RUN apt update \
    && pip install poetry \
    && apt install -y vim \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /market/backend \
    && chdir /market/backend \
    && poetry config virtualenvs.create false \
    && poetry install --only main

WORKDIR /market/backend/src

COPY --chown=app:app . /market/backend/

EXPOSE 8000

USER app

CMD ["sh", "/market/backend/entrypoint.sh"]
