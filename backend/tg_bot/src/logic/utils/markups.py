from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_product_type_markup() -> ReplyKeyboardBuilder:
    type_product_markup = ReplyKeyboardBuilder()
    type_product_markup.row(KeyboardButton(text='Нет типа'))
    type_product_markup.row(KeyboardButton(text='Букет'))
    type_product_markup.row(
        KeyboardButton(text='Коробка'),
        KeyboardButton(text='Корзинка'),
    )
    return type_product_markup
