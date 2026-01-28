from abc import ABC, abstractmethod


class PaymentAcceptServiceInterface(ABC):
    @abstractmethod
    def handle_webhook(self, request_data: dict) -> bool:
        raise NotImplementedError
