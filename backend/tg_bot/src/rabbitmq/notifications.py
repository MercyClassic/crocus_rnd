import asyncio

import pika

from config import get_config


class NotificationBus:
    def __init__(self):
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(get_config().PIKA_HOST),
        )
        self._channel = self.__connection.channel()
        self._channel.exchange_declare(
            exchange='notifications',
            exchange_type='direct',
        )

    def receive_notification(self):
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

    @staticmethod
    def order_callback(channel, method, properties, body: bytes):
        from handlers.notifications import new_order_notification

        loop = asyncio.new_event_loop()
        loop.run_until_complete(new_order_notification(int(body.decode('utf-8'))))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def call_me_callback(channel, method, properties, body: bytes):
        from handlers.notifications import new_call_me_request_notification

        loop = asyncio.new_event_loop()
        loop.run_until_complete(new_call_me_request_notification(body.decode('utf-8')))
        channel.basic_ack(delivery_tag=method.delivery_tag)
