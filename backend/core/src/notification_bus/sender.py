import functools
from abc import ABC, abstractmethod

from async_to_sync.run_with_loop import run_with_loop
from faststream.rabbit import RabbitBroker
from payments.domain.entities.order_id import OrderId


class NotificationBusInterface(ABC):
    @abstractmethod
    def order_created(self, order_id: OrderId) -> None:
        raise NotImplementedError

    @abstractmethod
    def call_me_requested(self, phone_number: str) -> None:
        raise NotImplementedError


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
    async def order_created(self, order_id: OrderId) -> None:
        await self._broker.publish(
            str(order_id),
            exchange='notifications',
            queue='order',
        )

    @run_with_loop
    @with_connection
    async def call_me_requested(self, phone_number: str) -> None:
        await self._broker.publish(
            phone_number,
            exchange='notifications',
            queue='call_me',
        )
