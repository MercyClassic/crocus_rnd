from abc import ABC, abstractmethod
from datetime import datetime


class PaymentCreateServiceInterface(ABC):
    @abstractmethod
    def create_payment(
            self,
            products: dict[str, int],
            amount: int,
            customer_name: str,
            customer_email: str,
            receiver_name: str | None,
            customer_phone_number: str,
            receiver_phone_number: str | None,
            without_calling: bool,
            delivery_address: str,
            delivery_date: datetime,
            delivery_time: str,
            note: str,
            cash: bool,
            delivering: bool,
    ) -> str | bool:
        raise NotImplementedError
