import pika

from config.settings import RABBITMQ_HOST


class NotificationBus:
    def __init__(self):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))

    def __enter__(self):
        self._channel = self.__connection.channel()
        self._channel.exchange_declare(
            exchange='notifications',
            exchange_type='direct',
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def send_order_notification(self, order_id: int) -> None:
        self._channel.basic_publish(
            exchange='notifications',
            routing_key='order',
            body=str(order_id).encode('utf-8'),
        )

    def send_call_me_request_notification(self, phone_number: str) -> None:
        self._channel.basic_publish(
            exchange='notifications',
            routing_key='call_me',
            body=phone_number.encode('utf-8'),
        )
