from abc import ABC, abstractmethod


class PaymentAcceptServiceInterface(ABC):
    @abstractmethod
    def handle_webhook(self) -> bool:
        raise NotImplementedError
