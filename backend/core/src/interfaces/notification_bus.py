from abc import ABC, abstractmethod


class NotificationBusInterface(ABC):
    @abstractmethod
    def send_order_notification(self, order_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_call_me_request_notification(self, phone_number: str) -> None:
        raise NotImplementedError
