from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    PIKA_HOST: str
    domain: str
    to_notificate_telegram_id: str
    admin_panel_product_url: str
    admin_panel_order_url: str
    admin_panel_category_url: str
    admin_panel_url: str


def get_config() -> Config:
    return Config()
