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
        self._bot = bot
        self._domain = domain
        self._admin_panel_order_url = admin_panel_order_url
        self._notification_receivers = notification_receivers

    async def order_created(self, order_id: int) -> None:
        markup = InlineKeyboardBuilder()
        url = f'{self._domain}{self._admin_panel_order_url % order_id}'
        markup.add(
            types.InlineKeyboardButton(text='Посмотреть детали заказа', url=url),
        )

        for telegram_id in self._notification_receivers:
            await self._bot.send_message(
                telegram_id,
                'У вас новый заказ!',
                reply_markup=markup.as_markup(),
            )

    async def call_me_requested(self, phone_number: str) -> None:
        for telegram_id in self._notification_receivers:
            await self._bot.send_message(
                telegram_id,
                f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
            )
