from faststream import Context
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from faststream.rabbit.router import RabbitRouter

from notification_bus.sender import NotificationSender

router = RabbitRouter()

exchange = RabbitExchange('notifications', type=ExchangeType.DIRECT)

queue_order = RabbitQueue('order')
queue_call_me = RabbitQueue('call_me')


@router.subscriber(queue=queue_order, exchange=exchange)
async def order_handler(
    order_id: int,
    notification_sender: NotificationSender = Context(),  # noqa: B008
):
    await notification_sender.new_order_notification(order_id)


@router.subscriber(queue=queue_call_me, exchange=exchange)
async def call_me_handler(
    phone_number: str,
    notification_sender: NotificationSender = Context(),  # noqa: B008
):
    await notification_sender.new_call_me_request_notification(phone_number)
