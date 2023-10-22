from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from download_image import download_photo

from utils import command_for


class ImageState(StatesGroup):
    image = State()


@command_for(permission_level='owner')
async def start_set_background_image(message):
    await ImageState.image.set()

    await bot.send_message(
        message.from_user.id,
        'Загрузите изображение',
    )


async def set_background_image(message, state):
    await state.finish()
    await download_photo(
        message.photo[-1].file_id,
        '../../../../frontend/build/static/img/jpg/bg.jpg',
    )
    await bot.send_message(
        message.from_user.id,
        'Главное изображение успешно загружено!',
    )


@command_for(permission_level='admin')
async def send_background_image(message):
    with open('../../../../frontend/build/static/img/jpg/bg.jpg', 'rb') as buffer:
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