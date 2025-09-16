from notification_bus.interfaces.sender import NotificationBusInterface

from payments.application.interfaces.services.call_me import CallMeServiceInterface


class CallMeService(CallMeServiceInterface):
    def __init__(self, notification_bus: NotificationBusInterface):
        self.notification_bus = notification_bus

    def create_call_me_request(self, phone_number: str) -> None:
        self.notification_bus.send_call_me_request_notification(phone_number)
