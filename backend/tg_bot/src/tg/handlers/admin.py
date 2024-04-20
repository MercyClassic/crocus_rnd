from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.utils.messages import admin_help_text
from logic.utils.utils import command_for

from config import Config

router = Router()


@command_for(permission_level='admin')
@router.message(Command('ahelp'))
async def admin_help(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        admin_help_text,
    )


@command_for(permission_level='admin')
@router.message(Command('adminpanel'))
async def open_admin_panel(
    message: types.Message,
    bot: Bot,
    config: Config,
):
    url = ''.join((config.domain, config.admin_panel_url))
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton(text='Перейти в админ панель', url=url))
    await bot.send_message(
        message.from_user.id,
        'Нажми меня',
        reply_markup=markup.as_markup(),
    )
