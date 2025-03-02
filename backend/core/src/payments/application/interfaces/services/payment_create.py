from abc import ABC, abstractmethod

from payments.application.models.order import OrderDTO


class PaymentCreateServiceInterface(ABC):
    @abstractmethod
    def create_payment(self, order_data: OrderDTO) -> str | bool:
        raise NotImplementedError
