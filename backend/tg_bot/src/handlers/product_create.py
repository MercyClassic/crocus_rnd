import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from dependency_injector.wiring import Provide, inject
from repositories.core import CoreRepository

from config import Config
from container import Container
from utils.download_image import download_photo
from utils.markups import type_product_markup
from utils.utils import command_for, slugify_string, validate_title


class ProductState(StatesGroup):
    title = State()
    slug = State()
    description = State()
    price = State()
    kind = State()
    image = State()
    extra_images = State()


@command_for(permission_level='owner')
async def create_product_start(message):
    await ProductState.title.set()

    await bot.send_message(
        message.from_user.id,
        'Создаём товар...\nСначала напишите название',
    )


async def set_title(message, state):
    if not validate_title(message.text):
        await bot.send_message(
            message.from_user.id,
            'В названии присутствуют недопустимые символы, попробуйте другое',
        )
        return
    async with state.proxy() as data:
        data['title'] = message.text
        data['slug'] = slugify_string(message.text)

    await ProductState.next()
    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Введите описание',
    )


async def set_description(message, state):
    async with state.proxy() as data:
        data['description'] = message.text

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Назначьте цену',
    )


async def set_price(message, state):
    try:
        int(message.text)
    except ValueError:
        await bot.send_message(
            message.from_user.id,
            'Цена должна состоять только из цифр, попробуйте ещё раз',
        )
        return None
    async with state.proxy() as data:
        data['price'] = message.text
    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        "Введите тип товара либо '-', если у товара нет типа",
        reply_markup=type_product_markup,
    )


async def set_kind(message, state):
    if message.text not in ('Нет типа', '-', 'Букет', 'Коробка', 'Корзинка'):
        await bot.send_message(
            message.from_user.id,
            'Тип не соответствует требованиям, попробуйте ещё раз',
            reply_markup=type_product_markup,
        )
        return None
    product_types = {
        'Нет букета': None,
        '-': None,
        'Букет': 'bouquet',
        'Коробка': 'box',
        'Корзинка': 'basket',
    }
    async with state.proxy() as data:
        data['kind'] = product_types.get(message.text)

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Добавьте главное изображение для товара',
    )


async def set_main_image(message, state):
    image = await download_photo(message.photo[-1].file_id)
    async with state.proxy() as data:
        data['image'] = image

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        "Добавьте дополнительные изображения одним сообщением либо напишите '-', если они не нужны",
    )


async def set_extra_images(  # noqa: CCR001
    message,
    state,
    album=None,
):
    if message.content_type == 'text':
        if message.text == '-':
            async with state.proxy() as data:
                data['extra_images'] = None
        else:
            await bot.send_message(message.from_user.id, 'Неверная команда')
    elif message.content_type == 'photo':
        if album:
            media_group = types.MediaGroup()
            for media_content in album:
                file_id = media_content.photo[-1].file_id
                try:
                    media_group.attach(
                        {'media': file_id, 'type': media_content.content_type},
                    )
                except ValueError:
                    return await message.answer(
                        'Возникла неизвестная ошибка, повторите попытку',
                    )
            image_ids = list(map(lambda obj: obj.photo[-1].file_id, album))
        else:
            image_ids = [message.photo[-1].file_id]

        extra_images = await asyncio.gather(
            *[download_photo(file_id) for file_id in image_ids],
        )
        async with state.proxy() as data:
            data['extra_images'] = extra_images

        await state.finish()
        await finish_product_create(data._data, message.from_user.id)


@inject
async def finish_product_create(
    data: dict,
    from_user_id: int,
    core_repo: CoreRepository = Provide[Container.core_repo],
    config: Config = Provide[Container.config],
):
    product_id, product_slug = await core_repo.create_product(data)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            'Перейти в админ панель товара',
            url=''.join(
                (config.domain, (config.admin_panel_product_url % product_id)),
            ),
        ),
    )
    markup.add(
        types.InlineKeyboardButton(
            'Посмотреть товар на сайте',
            url=''.join((config.domain, f'/flower/{product_slug}')),
        ),
    )

    await bot.send_message(
        from_user_id,
        'Готово, продукт создан!',
        reply_markup=markup,
    )


def register_product_create_handlers(dp: Dispatcher):
    dp.register_message_handler(create_product_start, commands=['createproduct'])
    dp.register_message_handler(set_title, state=ProductState.title)
    dp.register_message_handler(set_description, state=ProductState.description)
    dp.register_message_handler(set_price, state=ProductState.price)
    dp.register_message_handler(set_kind, state=ProductState.kind)
    dp.register_message_handler(
        set_main_image,
        state=ProductState.image,
        content_types=['photo'],
    )
    dp.register_message_handler(
        set_extra_images,
        state=ProductState.extra_images,
        content_types=['text', 'photo'],
    )
