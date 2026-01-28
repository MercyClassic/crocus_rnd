from abc import ABC, abstractmethod
from decimal import Decimal

from payments.domain.entities.order import OrderProduct
from payments.domain.entities.order_id import OrderId
from payments.domain.entities.value_objects import Money


class PaymentUrlGatewayInterface(ABC):
    @abstractmethod
    def get_payment_url(
        self,
        order_id: OrderId,
        amount: Money,
        customer_phone_number: str,
        products: list[OrderProduct],
        products_count: dict[str, int],
        with_delivery: bool,
        customer_email: str | None,
        discount_coefficient: Decimal,
    ) -> str | None:
        raise NotImplementedError
