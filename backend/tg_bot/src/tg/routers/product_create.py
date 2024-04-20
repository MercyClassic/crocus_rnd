import asyncio

from aiogram import Bot, F, Router, types
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from db.repositories import CoreRepository
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from main.config import Config

from tg.command_for import command_for

router = Router()


def slugify_string(string: str) -> str:
    return string.translate(
        str.maketrans(
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ’',
            'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA__',
        ),
    )


def validate_title(title: str) -> bool:
    return not any(i in '!@#$%^&*()+=`~;:"[]{}.,\'\\/' for i in title)


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


def get_product_type_keyboard() -> types.ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    markup.button(text='Нет типа')
    markup.button(text='Букет')
    markup.button(text='Коробка')
    markup.button(text='Корзинка')
    markup.adjust(1)
    return markup.as_markup(one_time_keyboard=True, resize_keyboard=True)


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
        return

    await state.update_data(price=int(message.text))
    await state.set_state(ProductState.kind)

    await bot.send_message(
        message.from_user.id,
        "Введите тип товара либо '-', если у товара нет типа",
        reply_markup=get_product_type_keyboard,
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
            reply_markup=get_product_type_keyboard,
        )
    else:
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
@inject
async def set_main_image(
    message: types.Message,
    bot: Bot,
    config: FromDishka[Config],
    state: FSMContext,
):
    file_id = message.photo[-1].file_id
    path = f'{config.media_dir}/{file_id}.jpg'
    await bot.download_file(file_id, path)

    await state.update_data(image=f'images/{file_id}.jpg')
    await state.set_state(ProductState.extra_images)

    await bot.send_message(
        message.from_user.id,
        "Добавьте дополнительные изображения одним сообщением"
        " либо напишите '-', если они не нужны",
    )


@router.message(
    ProductState.extra_images,
    F.content_type.in_([ContentType.TEXT, ContentType.PHOTO]),
)
@inject
async def set_extra_images(
    message: types.Message,
    bot: Bot,
    config: FromDishka[Config],
    core_repo: FromDishka[CoreRepository],
    state: FSMContext,
    album: list | None = None,
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
            *[bot.download_file(file.media, config.media_dir) for file in media_group],
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
