import functools

from async_to_sync.run_with_loop import run_with_loop
from faststream.rabbit import RabbitBroker

from notification_bus.interfaces.sender import NotificationBusInterface


def with_connection(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        await self._broker.connect()
        try:
            return await func(self, *args, **kwargs)
        finally:
            await self._broker.close()

    return wrapper


class NotificationBus(NotificationBusInterface):
    def __init__(self, broker_host_uri: str):
        self._broker = RabbitBroker(broker_host_uri)

    @run_with_loop
    @with_connection
    async def send_order_notification(self, order_id: int) -> None:
        await self._broker.publish(
            str(order_id),
            exchange='notifications',
            queue='order',
        )

    @run_with_loop
    @with_connection
    async def send_call_me_request_notification(self, phone_number: str) -> None:
        await self._broker.publish(
            phone_number,
            exchange='notifications',
            queue='call_me',
        )
