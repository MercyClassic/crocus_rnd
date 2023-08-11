from aiogram import Dispatcher, types
from django.urls import reverse

from bot.create_bot import bot, domain
from bot.messages import admin_help_text
from bot.utils import command_for


@command_for(permission_level='admin')
async def admin_help(message):
    await bot.send_message(
        message.from_user.id,
        admin_help_text,
    )


@command_for(permission_level='admin')
async def open_admin_panel(message):
    url = ''.join((domain, reverse('admin:index')))
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
