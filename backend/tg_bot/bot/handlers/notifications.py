import os

from aiogram import types
from create_bot import bot, domain
from django.urls import reverse


async def send_notification_about_new_order(order_id):
    markup = types.InlineKeyboardMarkup()
    url = domain + reverse('admin:payments_order_change', args=[order_id])
    markup.add(types.InlineKeyboardButton('Посмотреть детали заказа', url=url))

    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        'У вас новый заказ!',
        reply_markup=markup,
    )


async def send_notification_about_new_call_me(phone_number):
    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
    )
