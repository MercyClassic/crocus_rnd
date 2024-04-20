import pika


class NotificationBus:
    def __init__(self, host: str, port: int):
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port),
        )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange='notifications',
            exchange_type='direct',
        )

    def __del__(self):
        self.__connection.close()

    def send_order_notification(self, order_id: int) -> None:
        self.__channel.basic_publish(
            exchange='notifications',
            routing_key='order',
            body=str(order_id).encode('utf-8'),
        )

    def send_call_me_request_notification(self, phone_number: str) -> None:
        self.__channel.basic_publish(
            exchange='notifications',
            routing_key='call_me',
            body=phone_number.encode('utf-8'),
        )
