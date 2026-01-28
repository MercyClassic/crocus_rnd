from dishka import FromDishka
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from faststream.rabbit.router import RabbitRouter

from notification_bus.sender import NotificationSender

router = RabbitRouter()

exchange = RabbitExchange('notifications', type=ExchangeType.DIRECT)

queue_order = RabbitQueue('order')
queue_call_me = RabbitQueue('call_me')


@router.subscriber(queue=queue_order, exchange=exchange)
async def order_handler(
    order_id: str,
    notification_sender: FromDishka[NotificationSender],
):
    await notification_sender.order_created(order_id)


@router.subscriber(queue=queue_call_me, exchange=exchange)
async def call_me_handler(
    phone_number: str,
    notification_sender: FromDishka[NotificationSender],
):
    await notification_sender.call_me_requested(phone_number)
