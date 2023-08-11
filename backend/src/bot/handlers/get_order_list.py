from aiogram import Dispatcher, types
from aiogram.utils.callback_data import CallbackData

from bot.create_bot import bot
from bot.messages import get_order_detail_message
from bot.sql import get_paid_orders
from bot.utils import command_for

orders = None


callback_order = CallbackData('order', 'pk', 'action')


@command_for(permission_level='admin')
async def get_order_list(message):
    global orders
    orders = get_paid_orders()
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
        get_order_detail_message(order),
    )
    await callback.answer()


def register_get_order_list_handlers(dp: Dispatcher):
    dp.register_message_handler(get_order_list, commands=['orderlist'])
    dp.register_callback_query_handler(
        callback_order_detail,
        lambda cb: cb.data.split(':')[-1] == 'check_order_detail',
    )
