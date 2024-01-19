from rest_framework.request import Request

from rabbitmq.notification_bus import NotificationBus


class CallMeService:
    def __init__(self, notification_bus: NotificationBus):
        self.notification_bus = notification_bus

    def create_call_me_request(
        self,
        request: Request,
        phone_number: str,
    ) -> None:
        self.notification_bus.send_call_me_request_notification(phone_number)
