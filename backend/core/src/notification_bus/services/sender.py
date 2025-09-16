from faststream.rabbit import RabbitBroker

from async_to_sync.run_with_loop import run_with_loop
from notification_bus.interfaces.sender import NotificationBusInterface



class NotificationBus(NotificationBusInterface):
    def __init__(self, broker_host_uri: str):
        self._broker = RabbitBroker(broker_host_uri)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @run_with_loop
    async def connect(self) -> None:
        await self._broker.connect()

    @run_with_loop
    async def close(self) -> None:
        await self._broker.close()

    @run_with_loop
    async def send_order_notification(self, order_id: int) -> None:
        await self._broker.publish(
            str(order_id), exchange='notifications', queue='order'
        )

    @run_with_loop
    async def send_call_me_request_notification(self, phone_number: str) -> None:
        await self._broker.publish(
            phone_number, exchange='notifications', queue='call_me'
        )
