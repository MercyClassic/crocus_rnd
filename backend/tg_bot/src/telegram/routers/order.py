from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.repositories import CoreRepository
from dishka import FromDishka
from dto.order import OrderDTO

from telegram.command_for import command_for

router = Router()


class OrderDetail(CallbackData, prefix='order_detail'):
    order_id: int


@router.message(Command('orderlist'))
@command_for(permission_level='admin')
async def get_order_list(
    message: types.Message,
    bot: Bot,
    core_repo: FromDishka[CoreRepository],
) -> None:
    orders = await core_repo.get_orders()
    if orders:
        orders = {order.id: OrderDTO.model_validate(order) for order in orders}

        markup = InlineKeyboardBuilder()
        for order in orders.values():
            markup.button(
                text=f'{order.id} - {order.created_at} - {order.amount}р',
                callback_data=OrderDetail(order_id=order.id),
            )
        markup.adjust(1)

        await bot.send_message(
            message.from_user.id,
            'Нажмите на один из заказов ниже, чтобы посмотреть детали',
            reply_markup=markup.as_markup(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'Заказов нет',
        )

@router.callback_query(OrderDetail.filter())
async def callback_order_detail(
    callback: types.CallbackQuery,
    bot: Bot,
    callback_data: OrderDetail,
    core_repo: FromDishka[CoreRepository],
) -> None:
    order = await core_repo.get_order(order_id=callback_data.order_id)
    order = OrderDTO.model_validate(order)

    await bot.send_message(
        callback.message.chat.id,
        get_order_detail_message(order),
    )
    await callback.answer()


def get_order_detail_message(order: OrderDTO) -> str:
    products = ''
    for product_association in order.product_associations:
        products += (
            f'\t\t\t ‣ Название товара: {product_association.product.title},'
            f' Количетсво: {product_association.count}\n'
        )
    return (
        f'Информация о заказе:'
        f'\n • ID заказа: {order.id}'
        f'\n • Время создания заказа: {order.created_at}'
        f'\n • Сумма заказа: {order.amount}'
        f'\n • Ожидаемая дата получения: {order.delivery_date} '
        f'\n • Примечание: {order.note} '
        f'\n • С доставкой: {"Да" if order.delivering else "Нет"}'
        f'\n • Адрес доставки: {order.delivery_address} '
        f'\n • Время доставки: {order.delivery_time} '
        f'\n • Товары:\n{products}'
    )
