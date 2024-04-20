import os

from aiogram import Bot
from main import load_config
from notification_bus.notification_bus import NotificationBus
from notification_bus.sender import NotificationSender


def main():
    app_config = load_config()
    bot = Bot(app_config.bot_token)
    notification_sender = NotificationSender(
        bot=bot,
        config=app_config,
    )
    notification_bus = NotificationBus(
        host=os.environ['RABBITMQ_HOST'],
        port=int(os.environ['RABBITMQ_PORT']),
        notification_sender=notification_sender,
    )
    notification_bus.receive_notification()


if __name__ == '__main__':
    main()
