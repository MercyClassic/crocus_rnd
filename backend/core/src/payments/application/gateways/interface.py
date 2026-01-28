from abc import ABC, abstractmethod
from collections.abc import Iterable
from decimal import Decimal

from products.models import Product


class PaymentUrlGatewayInterface(ABC):
    @abstractmethod
    def get_payment_url(
            self,
            order_uuid: str,
            amount: int,
            customer_phone_number: str,
            products: Iterable[Product],
            products_count: dict[str, int],
            with_delivery: bool,
            customer_email: str | None,
            discount_coefficient: Decimal,
    ) -> str | None:
        raise NotImplementedError
