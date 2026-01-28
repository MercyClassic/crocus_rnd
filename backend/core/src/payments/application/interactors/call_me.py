from notification_bus.sender import NotificationBusInterface


class CallMeInteractor:
    def __init__(self, notification_bus: NotificationBusInterface):
        self.notification_bus = notification_bus

    def __call__(self, phone_number: str) -> None:
        self.notification_bus.call_me_requested(phone_number)
