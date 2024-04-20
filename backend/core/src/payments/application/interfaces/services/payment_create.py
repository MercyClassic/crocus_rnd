from abc import ABC, abstractmethod
from typing import List

from products.models import Product


class PaymentCreateServiceInterface(ABC):
    @abstractmethod
    def fill_in_with_data(self, serialized_data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_receipt(
        self,
        products: List[Product],
        with_delivery: bool = False,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        receipt: dict,
    ) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def create_payment(self) -> str | bool:
        raise NotImplementedError
