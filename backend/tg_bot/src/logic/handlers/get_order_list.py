from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.repositories import CoreRepository
from dto.order import OrderDTO
from logic.utils.messages import get_order_detail_message
from logic.utils.utils import command_for
from pydantic import TypeAdapter

router = Router()


orders = {}


class OrderDetail(CallbackData, prefix='order_detail'):
    order_id: int


@command_for(permission_level='admin')
@router.message(Command('orderlist'))
async def get_order_list(
    message: types.Message,
    bot: Bot,
    core_repo: CoreRepository,
):
    global orders
    orders = await core_repo.get_paid_orders()
    orders = {order.id: TypeAdapter(OrderDTO).validate_python(order) for order in orders}
    markup = InlineKeyboardBuilder()
    for order in orders.values():
        markup.button(
            text=f'{order.id}' f' - {order.created_at}' f' - {order.amount}р',
            callback_data=OrderDetail(order_id=order.id),
        )
    markup.adjust(1)

    await bot.send_message(
        message.from_user.id,
        'Нажмите на один из заказов ниже, чтобы посмотреть детали',
        reply_markup=markup.as_markup(),
    )


@router.callback_query(OrderDetail.filter())
async def callback_order_detail(
    callback: types.CallbackQuery,
    bot: Bot,
    callback_data: OrderDetail,
):
    pk = callback_data.order_id
    try:
        order = orders[pk]
    except KeyError:
        await bot.send_message(
            callback.message.chat.id,
            'Сначала вызовите команду /orderlist',
        )
        return

    await bot.send_message(
        callback.message.chat.id,
        get_order_detail_message(order),
    )
    await callback.answer()
