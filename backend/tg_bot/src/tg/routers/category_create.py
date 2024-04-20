from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import Config
from db.repositories import CoreRepository
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from tg.command_for import command_for

router = Router()


class CategoryState(StatesGroup):
    name = State()
    image = State()
    active = State()


@command_for(permission_level='owner')
@router.message(Command('createcategory'))
async def create_category_start(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    await state.set_state(CategoryState.name)

    await bot.send_message(
        message.from_user.id,
        'Создаём категорию...\nСначала напишите название',
    )


@router.message(CategoryState.name)
async def set_name(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    await state.update_data(name=message.text)
    await state.set_state(CategoryState.image)

    await bot.send_message(
        message.from_user.id,
        'Теперь загрузите изображение для данной категории',
    )


@router.message(CategoryState.image, F.photo)
@inject
async def set_image(
    message: types.Message,
    bot: Bot,
    config: FromDishka[Config],
    state: FSMContext,
):
    file_id = message.photo[-1].file_id
    path = f'{config.media_dir}/{file_id}.jpg'
    await bot.download_file(file_id, path)

    await state.update_data(image=f'images/{file_id}.jpg')
    await state.set_state(CategoryState.active)

    await bot.send_message(
        message.from_user.id,
        "Последний этап: будет ли категория активна?\nНапишите 'Да' или 'Нет'",
    )


@router.message(CategoryState.active)
@inject
async def set_active(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
    core_repo: FromDishka[CoreRepository],
    config: FromDishka[Config],
):
    text = message.text.lower()
    if text not in ('да', 'нет'):
        await bot.send_message(
            message.from_user.id,
            'Символы в сообщении не соответсвуют правильному ответу, попробуйте ещё раз',
        )
    else:
        data = await state.get_data()
        data['is_active'] = text == 'да'

        await state.clear()
        await finish_category_create(
            data,
            message.from_user.id,
            core_repo,
            config,
            bot,
        )


async def finish_category_create(
    data: dict,
    from_user_id: int,
    core_repo: CoreRepository,
    config: Config,
    bot: Bot,
):
    category_id = await core_repo.create_category(data)

    markup = InlineKeyboardBuilder()
    markup.add(
        types.InlineKeyboardButton(
            text='Перейти в админ панель товара',
            url=''.join(
                (config.domain, (config.admin_panel_category_url % category_id)),
            ),
        ),
    )

    await bot.send_message(
        from_user_id,
        'Готово! Категория создана!',
        reply_markup=markup.as_markup(),
    )
