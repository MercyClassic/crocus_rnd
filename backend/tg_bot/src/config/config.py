import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigParseError(ValueError):
    pass


@dataclass
class Config:
    db_uri: str
    bot_token: str
    rabbitmq_host: str
    to_notificate_telegram_id: str

    domain: str
    admin_panel_product_url: str
    admin_panel_order_url: str
    admin_panel_category_url: str
    admin_panel_url: str

    root_dir: str = '%s' % Path(__file__).parent.parent
    media_dir: str = '%s/%s' % (
        Path(__file__).parent.parent.parent.parent,
        'core/src/media/images',
    )
    bg_img_path: str = '%s/%s' % (
        Path(__file__).parent.parent.parent.parent.parent,
        'frontend/build/static/img/jpg/bg.jpg',
    )


def parse_from_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        logger.error(f'{key} is not set')
        raise ConfigParseError(f'{key} is not set')
    return value


def load_config() -> Config:
    return Config(
        db_uri=parse_from_env('db_uri'),
        bot_token=parse_from_env('BOT_TOKEN'),
        rabbitmq_host=parse_from_env('RABBITMQ_HOST'),
        domain=parse_from_env('DOMAIN'),
        to_notificate_telegram_id=parse_from_env('TO_NOTIFICATE_TELEGRAM_ID'),
        admin_panel_product_url=parse_from_env('ADMIN_PANEL_PRODUCT_URL'),
        admin_panel_order_url=parse_from_env('ADMIN_PANEL_ORDER_URL'),
        admin_panel_category_url=parse_from_env('ADMIN_PANEL_CATEGORY_URL'),
        admin_panel_url=parse_from_env('ADMIN_PANEL_URL'),
    )
