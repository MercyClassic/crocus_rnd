from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NotificationSender:
    def __init__(
        self,
        bot: Bot,
        domain: str,
        admin_panel_order_url: str,
        notification_receivers: list[int],
    ):
        self.bot = bot
        self.domain = domain
        self.admin_panel_order_url = admin_panel_order_url
        self.notification_receivers = notification_receivers

    async def new_order_notification(self, order_id: int) -> None:
        markup = InlineKeyboardBuilder()
        url = f'{self.domain}{self.admin_panel_order_url % order_id}'
        markup.add(
            types.InlineKeyboardButton(text='Посмотреть детали заказа', url=url)
        )

        for telegram_id in self.notification_receivers:
            await self.bot.send_message(
                telegram_id,
                'У вас новый заказ!',
                reply_markup=markup.as_markup(),
            )

    async def new_call_me_request_notification(self, phone_number: str) -> None:
        for telegram_id in self.notification_receivers:
            await self.bot.send_message(
                telegram_id,
                f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
            )
