from aiogram import types
from create_bot import bot
from dependency_injector.wiring import Provide, inject

from config import Config
from container import Container


@inject
async def new_order_notification(
    order_id: int,
    config: Config = Provide[Container.config],
):
    markup = types.InlineKeyboardMarkup()
    url = f'{config.domain}{config.admin_panel_order_url % order_id}'
    markup.add(types.InlineKeyboardButton('Посмотреть детали заказа', url=url))

    await bot.send_message(
        config.to_notificate_telegram_id,
        'У вас новый заказ!',
        reply_markup=markup,
    )


@inject
async def new_call_me_request_notification(
    phone_number: str,
    config: Config = Provide[Container.config],
):
    await bot.send_message(
        config.to_notificate_telegram_id,
        f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
    )
