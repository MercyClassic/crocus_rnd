from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from django.urls import reverse

from bot.create_bot import bot, domain
from bot.download_image import download_photo
from bot.utils import command_for, create_category


class CategoryState(StatesGroup):
    name = State()
    image = State()
    is_active = State()


@command_for(permission_level='owner')
async def create_category_start(message):
    await CategoryState.name.set()

    await bot.send_message(
        message.from_user.id,
        'Создаём категорию...\nСначала напишите название',
    )


async def set_name(message, state):
    async with state.proxy() as data:
        data['name'] = message.text

    await CategoryState.next()

    await bot.send_message(
        message.from_user.id,
        'Теперь загрузите изображение для данной категории',
    )


async def set_image(message, state):
    image = await download_photo(message.photo[-1].file_id)
    async with state.proxy() as data:
        data['image'] = image

    await CategoryState.next()

    await bot.send_message(
        message.from_user.id,
        "Последний этап: будет ли категория активна?\nНапишите 'Да' или 'Нет'",
    )


async def set_active(message, state):
    if message.text.lower() not in ('да', 'нет'):
        await bot.send_message(
            message.from_user.id,
            'Тип не соответствует требованиям, попробуйте ещё раз',
        )
        return
    is_active = {'да': True, 'нет': False}
    async with state.proxy() as data:
        data['is_active'] = is_active.get(message.text.lower())

    await state.finish()

    category_id = await create_category(data._data)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            'Перейти в админ панель товара',
            url=''.join(
                (domain, reverse('admin:products_category_change', args=[category_id])),
            ),
        ),
    )

    await bot.send_message(
        message.from_user.id,
        'Готово! Категория создана!',
        reply_markup=markup,
    )


def register_category_create_handlers(dp: Dispatcher):
    dp.register_message_handler(create_category_start, commands=['createcategory'])
    dp.register_message_handler(set_name, state=CategoryState.name)
    dp.register_message_handler(
        set_image,
        state=CategoryState.image,
        content_types=['photo'],
    )
    dp.register_message_handler(set_active, state=CategoryState.is_active)
