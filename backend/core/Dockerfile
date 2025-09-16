FROM python:3.11-slim-bookworm AS builder

COPY pyproject.toml poetry.lock ./

RUN apt update \
    && pip install poetry==1.8.3 \
    && apt install -y build-essential libmagic1 libmagic-dev \
    && poetry config virtualenvs.create false \
    && poetry install --only main \
    && rm -rf /var/lib/apt/lists/* /root/.cache

FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTEDECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -U app \
    && mkdir -p /app/backend/core/src \
    && chown -R app:app /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/

COPY --chown=app:app . /app/backend/core/

WORKDIR /app/backend/core/src

EXPOSE 8000

USER app

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
