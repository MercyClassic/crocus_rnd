from aiogram import Bot, Router, types
from aiogram.filters import Command

from config import Config

router = Router()


@router.message(Command('site'))
async def open_website(
    message: types.Message,
    bot: Bot,
    config: Config,
):
    await bot.send_message(
        message.from_user.id,
        config.domain,
    )


@router.message()
async def unknown_command(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        'Неизвестная команда. Проверьте сообщение на опечатку',
    )
