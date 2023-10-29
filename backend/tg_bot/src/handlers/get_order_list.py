from aiogram import Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from container import Container
from create_bot import bot
from dependency_injector.wiring import Provide, inject
from pydantic import TypeAdapter
from repositories.core import CoreRepository

from utils.messages import get_order_detail_message
from utils.schemas import OrderData
from utils.utils import command_for

orders = []

callback_order = CallbackData('order', 'pk', 'action')


@command_for(permission_level='admin')
@inject
async def get_order_list(
    message,
    core_repo: CoreRepository = Provide[Container.core_repo],
):
    global orders
    orders = await core_repo.get_paid_orders()
    markup = types.InlineKeyboardMarkup()
    orders = {order.id: TypeAdapter(OrderData).validate_python(order) for order in orders}
    for order in orders.values():
        markup.add(
            types.InlineKeyboardButton(
                text=f'{order.id}' f' - {order.created_at}' f' - {order.amount}р',
                callback_data=callback_order.new(
                    pk=order.id,
                    action='check_order_detail',
                ),
            ),
        )

    await bot.send_message(
        message.from_user.id,
        'Нажмите на один из заказов ниже, чтобы посмотреть детали',
        reply_markup=markup,
    )


async def callback_order_detail(callback):
    pk = callback.data.split(':')[1]
    try:
        order = orders[int(pk)]
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
