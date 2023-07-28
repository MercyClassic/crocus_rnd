import asyncio
import io
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from django.core.files.images import ImageFile
from django.urls import reverse
from PIL import Image

from bot import messages, sql
from bot.markups import type_product_markup
from bot.middlewares import AlbumMiddleware
from products.models import Category, Product, ProductImage

logger = logging.getLogger('telegram_errors')

bot = Bot(os.getenv('BOT_TOKEN'))
admin_ids = [int(admin_id) for admin_id in os.getenv('ADMIN_TG_BOT_IDS').split(', ')]
owner_ids = [int(owner_id) for owner_id in os.getenv('OWNER_TG_BOT_IDS').split(', ')]
domain = os.getenv('DOMAIN')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def command_for(permission_level: str):
    def decorator(func):
        def wrapper(*args):
            message = args[0]
            if (
                    (permission_level == 'admin' and message.from_user.id in admin_ids)
                    or (permission_level == 'owner' and message.from_user.id in owner_ids)
            ):
                return func(*args)
            return unknown_command(message)
        return wrapper
    return decorator


async def send_notification_about_new_order(order_id):
    markup = types.InlineKeyboardMarkup()
    url = domain + reverse('admin:payments_order_change', args=[order_id])
    markup.add(types.InlineKeyboardButton('Посмотреть детали заказа', url=url))

    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        'У вас новый заказ!',
        reply_markup=markup,
    )


async def send_notification_about_new_call_me(phone_number):
    await bot.send_message(
        os.getenv('TO_NOTIFICATE_TELEGRAM_ID'),
        f'Посетитель сайта попросил перезвонить ему на номер: {phone_number}',
    )


@dp.message_handler(commands=['site'])
async def open_website(message):
    await bot.send_message(
        message.from_user.id,
        domain,
    )


@dp.message_handler(commands=['ahelp'])
@command_for(permission_level='admin')
async def admin_help(message):
    await bot.send_message(
        message.from_user.id,
        messages.admin_help_text,
    )


callback_order = CallbackData('order', 'pk', 'action')

orders = None


@dp.message_handler(commands=['orderlist'])
@command_for(permission_level='admin')
async def get_order_list(message):
    orders = sql.get_paid_orders()
    markup = types.InlineKeyboardMarkup()
    for order in orders:
        markup.add(types.InlineKeyboardButton(
            text=f'{order.id} - {order.created_at} - {order.amount}р',
            callback_data=callback_order.new(pk=order.id, action='check_order_detail'),
        ))

    await bot.send_message(
        message.from_user.id,
        'Нажмите на один из заказов ниже, чтобы посмотреть детали',
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda cb: cb.data.split(':')[-1] == 'check_order_detail')
async def callback_order_detail(callback):
    pk = callback.data.split(':')[1]
    try:
        order = list(filter(lambda order: order.id == int(pk), orders))[0]
    except NameError:
        await bot.send_message(
            callback.message.chat.id,
            'Сначала вызовите команду /orderlist',
        )
        return None

    await bot.send_message(
        callback.message.chat.id,
        messages.get_order_detail_message(order),
    )
    await callback.answer()


@dp.message_handler(commands=['adminpanel'])
@command_for(permission_level='admin')
async def open_admin_panel(message):
    url = ''.join((domain, reverse('admin:index')))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти в админ панель', url=url))
    await bot.send_message(
        message.from_user.id,
        'Нажми меня',
        reply_markup=markup,
    )


class ProductState(StatesGroup):
    title = State()
    slug = State()
    description = State()
    price = State()
    type = State()
    image = State()
    extra_images = State()


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.reply('Создание отменено')


@dp.message_handler(commands=['createproduct'])
@command_for(permission_level='owner')
async def create_product_start(message):
    await ProductState.title.set()

    await bot.send_message(
        message.from_user.id,
        'Создаём товар...\nСначала напишите название',
    )


def slugify_title(string: str) -> str:
    return string.translate(
        str.maketrans(
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ',
            'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA_',
        ),
    )


def validate_title(title: str) -> bool:
    forbidden_characters = '!@#$%^&*()+=`~;:"[]{}.,m\\/'
    for char in title:
        if char in forbidden_characters:
            return False
    return True


@dp.message_handler(state=ProductState.title)
async def set_title(message, state):
    if not validate_title(message.text):
        await bot.send_message(
            message.from_user.id,
            'В названии присутствуют недопустимые символы, попробуйте другое',
        )
        return
    async with state.proxy() as data:
        data['title'] = message.text
        data['slug'] = slugify_title(message.text)

    await ProductState.next()
    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Введите описание',
    )


@dp.message_handler(state=ProductState.description)
async def set_description(message, state):
    async with state.proxy() as data:
        data['description'] = message.text

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Назначьте цену',
    )


@dp.message_handler(state=ProductState.price)
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
        'Введите тип товара либо "-", если у товара нет типа',
        reply_markup=type_product_markup,
    )


@dp.message_handler(state=ProductState.type)
async def set_type(message, state):
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
        data['type'] = product_types.get(message.text)

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Добавьте главное изображение для товара',
    )


async def download_photo(file_id):
    uri_info = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id='
    uri = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/'
    async with aiohttp.ClientSession() as request:
        async with request.get(uri_info + file_id) as response:
            img_path = (await response.json())['result']['file_path']
        async with request.get(uri + img_path) as img:
            return ImageFile(io.BytesIO(await img.content.read()), name=f'{file_id}.jpg')


@dp.message_handler(state=ProductState.image, content_types=['photo'])
async def set_main_image(message, state):
    image = await download_photo(message.photo[-1].file_id)
    async with state.proxy() as data:
        data['image'] = image

    await ProductState.next()

    await bot.send_message(
        message.from_user.id,
        'Добавьте дополнительные изображения одним сообщением либо напишите "-", если они не нужны',
    )


@dp.message_handler(state=ProductState.extra_images, content_types=['photo'])
async def set_extra_images(message, state, album=None):
    if album:
        media_group = types.MediaGroup()
        for media_content in album:
            file_id = media_content.photo[-1].file_id
            try:
                media_group.attach({'media': file_id, 'type': media_content.content_type})
            except ValueError:
                return await message.answer('Возникла неизвестная ошибка, повторите попытку')
        image_ids = list(map(lambda obj: obj.photo[-1].file_id, album))
    else:
        image_ids = [message.photo[-1].file_id]

    extra_images = await asyncio.gather(*[download_photo(file_id) for file_id in image_ids])

    async with state.proxy() as data:
        data['extra_images'] = extra_images

    await state.finish()

    product = await Product.objects.acreate(
        title=data['title'],
        slug=data['slug'],
        description=data['description'],
        price=data['price'],
        type=data['type'],
        image=data['image'],
    )
    product_images = []
    for i in extra_images:
        product_images.append(ProductImage(image=i, product=product))
    await sync_to_async(ProductImage.objects.bulk_create)(product_images)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Перейти в админ панель товара',
        url=''.join((domain, reverse('admin:products_product_change', args=[product.id]))),
    ))
    markup.add(types.InlineKeyboardButton(
        'Посмотреть товар на сайте',
        url=''.join((domain, reverse('products:product-detail', args=[product.id]))),
    ))

    await bot.send_message(
        message.from_user.id,
        'Готово, продукт создан!',
        reply_markup=markup,
    )


class CategoryState(StatesGroup):
    name = State()
    image = State()
    is_active = State()


@dp.message_handler(commands=['createcategory'])
@command_for(permission_level='owner')
async def create_category_start(message):
    await CategoryState.name.set()

    await bot.send_message(
        message.from_user.id,
        'Создаём категорию...\nСначала напишите название',
    )


@dp.message_handler(state=CategoryState.name)
async def set_name(message, state):
    async with state.proxy() as data:
        data['name'] = message.text

    await CategoryState.next()

    await bot.send_message(
        message.from_user.id,
        'Теперь загрузите изображение для данной категории',
    )


@dp.message_handler(state=CategoryState.image, content_types=['photo'])
async def set_image(message, state):
    image = await download_photo(message.photo[-1].file_id)
    async with state.proxy() as data:
        data['image'] = image

    await CategoryState.next()

    await bot.send_message(
        message.from_user.id,
        'Последний этап: будет ли категория активна?\nНапишите "Да" или "Нет"',
    )


@dp.message_handler(state=CategoryState.is_active)
async def set_active(message, state):
    if message.text.lower() not in ('да', 'нет'):
        await bot.send_message(
            message.from_user.id,
            'Тип не соответствует требованиям, попробуйте ещё раз',
        )
        return
    is_active = {'да': True, 'нет': False}
    async with state.proxy() as data:
        data['is_active'] = is_active.get(message.text)

    await state.finish()

    category = await Category.objects.acreate(
        name=data['name'],
        image=data['image'],
        is_active=data['is_active'],
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Перейти в админ панель товара',
        url=''.join((domain, reverse('admin:products_category_change', args=[category.id]))),
    ))

    await bot.send_message(
        message.from_user.id,
        'Готово! Категория создана!',
        reply_markup=markup,
    )


class ImageState(StatesGroup):
    image = State()


@dp.message_handler(commands=['setbgimage'])
@command_for(permission_level='owner')
async def start_set_background_image(message):
    await ImageState.image.set()

    await bot.send_message(
        message.from_user.id,
        'Загрузите изображение',
    )


@dp.message_handler(state=ImageState.image, content_types=['photo'])
async def set_background_image(message, state):
    await state.finish()
    image = await download_photo(message.photo[-1].file_id)
    img = Image.open(io.BytesIO(image.file.read()))
    img.thumbnail((2000, 1000))
    img.save('static/products/img/bg.jpg')
    await bot.send_message(
        message.from_user.id,
        'Главное изображение успешно загружено!',
    )


@dp.message_handler(commands=['downloadbgimage'])
@command_for(permission_level='admin')
async def send_background_image(message):
    with open('static/products/img/bg.jpg', 'rb') as buffer:
        await bot.send_photo(
            message.from_user.id,
            buffer,
        )


@dp.message_handler(content_types=[ContentType.ANY])
async def unknown_command(message):
    await bot.send_message(
        message.from_user.id,
        'Неизвестная команда. Проверьте сообщение на опечатку',
    )


@dp.errors_handler()
async def errors_handler(update, exception):
    logger.error(exception, extra={
        'user_id': update.message.from_user.id,
        'message_id': update.message.message_id,
    })
    return True


def bot_run():
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    bot_run()
