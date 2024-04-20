from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from main.config import Config

from tg.command_for import command_for

router = Router()


class ImageState(StatesGroup):
    image = State()


@command_for(permission_level='owner')
@router.message(Command('setbgimage'))
async def start_set_background_image(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    await state.set_state(ImageState.image)

    await bot.send_message(
        message.from_user.id,
        'Загрузите изображение',
    )


@router.message(ImageState.image, F.photo)
@inject
async def set_background_image(
    message: types.Message,
    bot: Bot,
    config: FromDishka[Config],
    state: FSMContext,
):
    await state.clear()
    file_id = message.photo[-1].file_id
    path = f'{config.bg_img_path}/{file_id}.jpg'
    await bot.download_file(file_id, path)
    await bot.send_message(
        message.from_user.id,
        'Главное изображение успешно загружено!',
    )


@command_for(permission_level='admin')
@router.message(Command('downloadbgimage'))
async def send_background_image(
    message: types.Message,
    bot: Bot,
    config: Config,
):
    image = types.FSInputFile(config.bg_img_path)
    await bot.send_photo(
        message.from_user.id,
        image,
    )
