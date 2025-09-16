from aiogram import Bot
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from main import load_config
from notification_bus.notification_bus import router
from notification_bus.sender import NotificationSender


def create_app():
    app_config = load_config()

    broker = RabbitBroker(app_config.broker_host_uri)
    broker.include_router(router)
    app = FastStream(broker)
    app.context.set_global(
        'notification_sender',
        NotificationSender(
            bot=Bot(app_config.bot_token),
            domain=app_config.domain,
            admin_panel_order_url=app_config.admin_panel_order_url,
            notification_receivers=app_config.to_notificate_telegram_ids,
        ),
    )
    return app


app = create_app()
