from aiogram import types

type_product_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
type_product_markup.row(types.KeyboardButton(text='Нет типа'))
type_product_markup.row(types.KeyboardButton(text='Букет'))
type_product_markup.row(
    types.KeyboardButton(text='Коробка'),
    types.KeyboardButton(text='Корзинка'),
)
