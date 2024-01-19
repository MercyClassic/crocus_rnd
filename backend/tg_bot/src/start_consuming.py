import os

from aiogram import Bot
from logic.handlers.notifications import NotificationSender
from logic.rabbitmq.notification_bus import NotificationBus

from config import load_config


def main():
    app_config = load_config()
    bot = Bot(app_config.bot_token)
    notification_sender = NotificationSender(
        bot=bot,
        config=app_config,
    )
    notification_bus = NotificationBus(
        host=os.environ['RABBITMQ_HOST'],
        port=5672,
        notification_sender=notification_sender,
    )
    notification_bus.receive_notification()


if __name__ == '__main__':
    main()
