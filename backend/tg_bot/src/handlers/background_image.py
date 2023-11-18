from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from dependency_injector.wiring import Provide, inject

from config import Config
from container import Container
from utils.download_image import download_photo
from utils.utils import command_for


class ImageState(StatesGroup):
    image = State()


@command_for(permission_level='owner')
async def start_set_background_image(message):
    await ImageState.image.set()

    await bot.send_message(
        message.from_user.id,
        'Загрузите изображение',
    )


@inject
async def set_background_image(
    message,
    state,
    config: Config = Provide[Container.config],
):
    await state.finish()
    await download_photo(
        message.photo[-1].file_id,
        config.BG_IMG_PATH,
    )
    await bot.send_message(
        message.from_user.id,
        'Главное изображение успешно загружено!',
    )


@command_for(permission_level='admin')
@inject
async def send_background_image(
    message,
    config: Config = Provide[Container.config],
):
    with open(config.BG_IMG_PATH, 'rb') as buffer:
        await bot.send_photo(
            message.from_user.id,
            buffer,
        )


def register_background_image_handlers(dp: Dispatcher):
    dp.register_message_handler(start_set_background_image, commands=['setbgimage'])
    dp.register_message_handler(
        set_background_image,
        state=ImageState.image,
        content_types=['photo'],
    )
    dp.register_message_handler(send_background_image, commands=['downloadbgimage'])
