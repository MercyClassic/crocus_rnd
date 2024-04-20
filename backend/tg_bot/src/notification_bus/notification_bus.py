import asyncio

import pika

from notification_bus.sender import NotificationSender


class NotificationBus:
    def __init__(
        self,
        host: str,
        port: int,
        notification_sender: NotificationSender,
    ) -> None:
        self.notification_sender = notification_sender
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port),
        )
        self._channel = self.__connection.channel()
        self._channel.exchange_declare(
            exchange='notifications',
            exchange_type='direct',
        )

    def receive_notification(self) -> None:
        callme_queue = self._channel.queue_declare(queue='call_me_notifications')
        order_queue = self._channel.queue_declare(queue='order_notifications')
        self._channel.queue_bind(
            exchange='notifications',
            queue=callme_queue.method.queue,
            routing_key='call_me',
        )
        self._channel.queue_bind(
            exchange='notifications',
            queue=order_queue.method.queue,
            routing_key='order',
        )
        self._channel.basic_consume(order_queue.method.queue, self.order_callback)
        self._channel.basic_consume(callme_queue.method.queue, self.call_me_callback)
        self._channel.start_consuming()

    def order_callback(
        self,
        channel,
        method,
        properties,
        body: bytes,
    ) -> None:
        loop = asyncio.get_event_loop()
        coro = self.notification_sender.new_order_notification(int(body.decode('utf-8')))
        loop.run_until_complete(coro)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def call_me_callback(
        self,
        channel,
        method,
        properties,
        body: bytes,
    ) -> None:
        loop = asyncio.get_event_loop()
        coro = self.notification_sender.new_call_me_request_notification(body.decode('utf-8'))
        loop.run_until_complete(coro)
        channel.basic_ack(delivery_tag=method.delivery_tag)
