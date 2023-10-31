from aiogram import Dispatcher
from aiogram.types import ContentType
from create_bot import bot
from dependency_injector.wiring import Provide, inject

from config import Config
from container import Container


@inject
async def open_website(
    message,
    config: Config = Provide[Container.config],
):
    await bot.send_message(
        message.from_user.id,
        config.domain,
    )


async def unknown_command(message):
    await bot.send_message(
        message.from_user.id,
        'Неизвестная команда. Проверьте сообщение на опечатку',
    )


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(open_website, commands=['site'])
    dp.register_message_handler(unknown_command, content_types=[ContentType.ANY])
