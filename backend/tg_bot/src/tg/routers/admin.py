from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from main.config import Config

from tg.command_for import command_for

router = Router()


@router.message()
async def unknown_command(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        'Неизвестная команда. Проверьте сообщение на опечатку',
    )


@command_for(permission_level='admin')
@router.message(Command('ahelp'))
async def admin_help(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        'Доступные команды:'
        '\n/orderlist - Посмотреть оплаченные неготовые заказазы'
        '\n/adminpanel - Открыть административную панель'
        '\n/createproduct - Создать товар'
        '\n/createcategory - Создать категорию'
        '\n/cancel - Отменить создание'
        '\n/setbgimage - Поменять главное изображение'
        '\n/downloadbgimage - Скачать главное изображение',
    )


@command_for(permission_level='admin')
@router.message(Command('adminpanel'))
async def open_admin_panel(
    message: types.Message,
    bot: Bot,
    config: Config,
):
    url = f'{config.domain}{config.admin_panel_url}'
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton(text='Перейти в админ панель', url=url))
    await bot.send_message(
        message.from_user.id,
        'Нажми меня',
        reply_markup=markup.as_markup(),
    )
