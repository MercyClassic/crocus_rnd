from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config


class NotificationSender:
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    async def new_order_notification(self, order_id: int) -> None:
        markup = InlineKeyboardBuilder()
        url = f'{self.config.domain}{self.config.admin_panel_order_url % order_id}'
        markup.add(types.InlineKeyboardButton(text='Посмотреть детали заказа', url=url))

        await self.bot.send_message(
            self.config.to_notificate_telegram_id,
            'У вас новый заказ!',
            reply_markup=markup.as_markup(),
        )

    async def new_call_me_request_notification(self, phone_number: str) -> None:
        await self.bot.send_message(
            self.config.to_notificate_telegram_id,
            f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
        )
