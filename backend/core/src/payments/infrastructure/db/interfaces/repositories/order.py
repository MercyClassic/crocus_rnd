from typing import Iterable

from accounts.schemas import UserDTO
from payments.infrastructure.db.models import Order
from payments.application.models.order import OrderDTO
from products.models import Product


class PaymentRepositoryInterface:
    def create_order(
        self,
        amount: int,
        data: OrderDTO,
        user_account: UserDTO,
    ) -> Order:
        raise NotImplementedError

    def get_order_products(
        self,
        products_slug: Iterable[str],
    ) -> Iterable[Product]:
        raise NotImplementedError

    def create_order_products(
        self,
        order_id: int,
        order_products: Iterable[Product],
        products_count: dict[str, int],
    ) -> None:
        raise NotImplementedError

    def get_order_by_uuid(self, uuid: str) -> Order | None:
        raise NotImplementedError

    def delete_order(self, uuid: str) -> None:
        raise NotImplementedError

    def set_is_paid_to_order(self, order: Order) -> None:
        raise NotImplementedError
