import json
import logging.config
import os
from dataclasses import dataclass
from pathlib import Path

import sentry_sdk

logs_path = Path(__file__).parent / 'logs'
if not logs_path.exists():
    logs_path.mkdir()

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    environment=os.environ['SENTRY_ENVIRONMENT'],
)

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main': {
                'format': '[{levelname}] {asctime} - {message}',
                'style': '{',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1_048_576,
                'backupCount': 50,
                'formatter': 'main',
                'filename': f'{logs_path}/telegram_error.log',
            },
            'console': {
                'level': 'INFO',
                'formatter': 'main',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'main': {
                'handlers': ['file', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    db_uri: str
    bot_token: str
    broker_host_uri: str
    to_notificate_telegram_ids: list[int]

    domain: str
    admin_panel_product_url: str
    admin_panel_order_url: str
    admin_panel_category_url: str
    admin_panel_url: str

    root_dir: str = str(Path(__file__).parent.parent)
    media_dir: str = '{}/{}'.format(  # noqa: RUF009
        Path(__file__).parent.parent.parent,
        'core/src/media/images',
    )
    bg_img_path: str = '{}/{}'.format(  # noqa: RUF009
        Path(__file__).parent.parent.parent.parent,
        'frontend/build/static/img/jpg/bg.jpg',
    )


def parse_from_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        logger.error(f'{key} is not set')
        raise ValueError(f'{key} is not set')
    return value


def load_config() -> Config:
    return Config(
        db_uri=parse_from_env('DB_URI'),
        bot_token=parse_from_env('BOT_TOKEN'),
        broker_host_uri=parse_from_env('RABBITMQ_URI'),
        domain=parse_from_env('DOMAIN'),
        to_notificate_telegram_ids=[
            int(t_id) for t_id in json.loads(os.environ['TO_NOTIFICATE_TELEGRAM_ID'])
        ],
        admin_panel_product_url=parse_from_env('ADMIN_PANEL_PRODUCT_URL'),
        admin_panel_order_url=parse_from_env('ADMIN_PANEL_ORDER_URL'),
        admin_panel_category_url=parse_from_env('ADMIN_PANEL_CATEGORY_URL'),
        admin_panel_url=parse_from_env('ADMIN_PANEL_URL'),
    )
