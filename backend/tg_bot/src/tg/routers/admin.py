from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import Config
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from tg.command_for import command_for

router = Router()


@router.message(Command('ahelp'))
@command_for(permission_level='admin')
async def admin_help(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        'Доступные команды:'
        '\n/orderlist - Посмотреть заказазы за последние 3 месяца'
        '\n/adminpanel - Открыть административную панель'
        '\n/createproduct - Создать товар'
        '\n/createcategory - Создать категорию'
        '\n/cancel - Отменить создание'
        '\n/setbgimage - Поменять главное изображение'
        '\n/downloadbgimage - Скачать главное изображение',
    )


@router.message(Command('adminpanel'))
@command_for(permission_level='admin')
@inject
async def open_admin_panel(
    message: types.Message,
    bot: Bot,
    config: FromDishka[Config],
):
    url = f'{config.domain}{config.admin_panel_url}'
    markup = InlineKeyboardBuilder()
    markup.add(types.InlineKeyboardButton(text='Перейти в админ панель', url=url))
    await bot.send_message(
        message.from_user.id,
        'Нажми меня',
        reply_markup=markup.as_markup(),
    )
