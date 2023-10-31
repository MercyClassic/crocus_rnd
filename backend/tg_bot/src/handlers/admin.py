from aiogram import Dispatcher, types
from create_bot import bot
from dependency_injector.wiring import Provide, inject

from config import Config
from container import Container
from utils.messages import admin_help_text
from utils.utils import command_for


@command_for(permission_level='admin')
async def admin_help(message):
    await bot.send_message(
        message.from_user.id,
        admin_help_text,
    )


@command_for(permission_level='admin')
@inject
async def open_admin_panel(message, config: Config = Provide[Container.config]):
    url = ''.join((config.domain, config.admin_panel_url))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти в админ панель', url=url))
    await bot.send_message(
        message.from_user.id,
        'Нажми меня',
        reply_markup=markup,
    )


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_help, commands=['ahelp'])
    dp.register_message_handler(open_admin_panel, commands=['adminpanel'])
