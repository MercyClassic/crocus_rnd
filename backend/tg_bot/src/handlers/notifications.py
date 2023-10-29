import os

from aiogram import types
from create_bot import admin_panel_order_url, bot, domain


async def send_notification_about_new_order(order_id: int):
    markup = types.InlineKeyboardMarkup()
    url = f'{domain}{admin_panel_order_url % order_id}'
    markup.add(types.InlineKeyboardButton('Посмотреть детали заказа', url=url))

    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        'У вас новый заказ!',
        reply_markup=markup,
    )


async def send_notification_about_new_call_me(phone_number: str):
    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
    )
