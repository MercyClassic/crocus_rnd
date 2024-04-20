import asyncio

from aiogram import Bot, F, Router, types
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.repositories import CoreRepository
from logic.utils.download_image import download_photo
from logic.utils.markups import get_product_type_markup
from logic.utils.utils import command_for, slugify_string, validate_title

from config import Config

router = Router()


class ProductState(StatesGroup):
    title = State()
    slug = State()
    description = State()
    price = State()
    kind = State()
    image = State()
    extra_images = State()


@command_for(permission_level='owner')
@router.message(Command('createproduct'))
async def create_product_start(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    await state.set_state(ProductState.title)

    await bot.send_message(
        message.from_user.id,
        'Создаём товар...\nСначала напишите название',
    )


@router.message(ProductState.title)
async def set_title(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    if not validate_title(message.text):
        await bot.send_message(
            message.from_user.id,
            'В названии присутствуют недопустимые символы, попробуйте другое',
        )
        return

    await state.update_data(
        title=message.text,
        slug=slugify_string(message.text),
    )

    await state.set_state(ProductState.description)
    await bot.send_message(
        message.from_user.id,
        'Введите описание',
    )


@router.message(ProductState.description)
async def set_description(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    await state.update_data(description=message.text)
    await state.set_state(ProductState.price)

    await bot.send_message(
        message.from_user.id,
        'Назначьте цену',
    )


@router.message(ProductState.price)
async def set_price(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    try:
        int(message.text)
    except ValueError:
        await bot.send_message(
            message.from_user.id,
            'Цена должна состоять только из цифр, попробуйте ещё раз',
        )
        return None

    await state.update_data(price=int(message.text))
    await state.set_state(ProductState.kind)

    await bot.send_message(
        message.from_user.id,
        "Введите тип товара либо '-', если у товара нет типа",
        reply_markup=get_product_type_markup().as_markup(one_time_keyboard=True),
    )


@router.message(ProductState.kind)
async def set_kind(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
):
    if message.text not in ('Нет типа', '-', 'Букет', 'Коробка', 'Корзинка'):
        await bot.send_message(
            message.from_user.id,
            'Тип не соответствует требованиям, попробуйте ещё раз',
            reply_markup=get_product_type_markup().as_markup(one_time_keyboard=True),
        )
        return None

    product_types = {
        'Нет букета': None,
        '-': None,
        'Букет': 'bouquet',
        'Коробка': 'box',
        'Корзинка': 'basket',
    }

    await state.update_data(kind=product_types.get(message.text))
    await state.set_state(ProductState.image)

    await bot.send_message(
        message.from_user.id,
        'Добавьте главное изображение для товара',
    )


@router.message(ProductState.image, F.photo)
async def set_main_image(
    message: types.Message,
    bot: Bot,
    config: Config,
    state: FSMContext,
):
    print('DO IMAGE DOWNLOAD')
    image = await download_photo(message.photo[-1].file_id, config)
    print('POSLE IMAGE DOWNLOAD')
    await state.update_data(image=image)
    await state.set_state(ProductState.extra_images)

    await bot.send_message(
        message.from_user.id,
        'Добавьте дополнительные изображения одним сообщением'
        " либо напишите '-', если они не нужны",
    )


@router.message(
    ProductState.extra_images,
    F.content_type.in_([ContentType.TEXT, ContentType.PHOTO]),
)
async def set_extra_images(
    message: types.Message,
    bot: Bot,
    config: Config,
    core_repo: CoreRepository,
    state: FSMContext,
    album: list = None,
):
    if message.content_type == 'text':
        if message.text == '-':
            await state.update_data(extra_images=None)
        else:
            await bot.send_message(
                message.from_user.id,
                'Неверная команда',
            )
            return
    elif message.content_type == 'photo':
        media_group = []
        for msg in album:
            file_id = msg.photo[-1].file_id
            media_group.append(types.InputMediaPhoto(media=file_id))

        extra_images = await asyncio.gather(
            *[download_photo(file.media, config) for file in media_group],
        )
        await state.update_data(extra_images=extra_images)

    data = await state.get_data()
    await state.clear()

    await finish_product_create(
        data,
        message.from_user.id,
        core_repo,
        config,
        bot,
    )


async def finish_product_create(
    data: dict,
    from_user_id: int,
    core_repo: CoreRepository,
    config: Config,
    bot: Bot,
):
    product_id, product_slug = await core_repo.create_product(data)

    markup = InlineKeyboardBuilder()
    markup.add(
        types.InlineKeyboardButton(
            text='Перейти в админ панель товара',
            url=''.join(
                (config.domain, (config.admin_panel_product_url % product_id)),
            ),
        ),
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Посмотреть товар на сайте',
            url=''.join((config.domain, f'/flower/{product_slug}')),
        ),
    )

    await bot.send_message(
        from_user_id,
        'Готово, продукт создан!',
        reply_markup=markup.as_markup(),
    )
