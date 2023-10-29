FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /market/backend/core/src/media/images
RUN mkdir -p /market/backend/tg_bot
RUN mkdir -p /market/frontend/build/static/img

COPY ./pyproject.toml /market/backend/tg_bot

RUN apt update \
    && pip install poetry \
    && apt install -y vim \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /market \
    && chdir /market/backend/tg_bot \
    && poetry config virtualenvs.create false \
    && poetry install --only main

COPY --chown=app:app . /market/backend/tg_bot

WORKDIR /market/backend/tg_bot/src

USER app

CMD ["python", "main.py"]
