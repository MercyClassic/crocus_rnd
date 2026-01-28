from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from main.config import load_config
from notification_bus.handlers import router
from main.provider import CoreProvider


def create_app():
    app_config = load_config()

    broker = RabbitBroker(app_config.broker_host_uri)
    broker.include_router(router)
    app = FastStream(broker)
    container = make_async_container(CoreProvider())
    setup_dishka(container, app, auto_inject=True)
    return app


app = create_app()
