FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /market

COPY ./pyproject.toml /market/pyproject.toml

RUN apt update \
    && pip install poetry \
    && apt install -y nano \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /market \
    && chdir /market \
    && poetry config virtualenvs.create false \
    && poetry install --only main

WORKDIR /market/src

COPY --chown=app:app . /market

EXPOSE 8000

USER app

CMD ["sh", "/market/entrypoint.sh"]
