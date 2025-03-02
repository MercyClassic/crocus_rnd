from collections.abc import Iterable

from accounts.schemas import UserDTO
from products.models import Product

from payments.application.models.order import OrderDTO
from payments.infrastructure.db.models import Order, PromoCode


class PaymentRepositoryInterface:
    def create_order(
        self,
        amount: int,
        data: OrderDTO,
        user_account: UserDTO,
        promo_code: PromoCode | None,
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

    def get_promo_code(self, promo_code: str) -> PromoCode | None:
        raise NotImplementedError

    def delete_order(self, uuid: str) -> None:
        raise NotImplementedError

    def set_is_paid_to_order(self, order: Order) -> None:
        raise NotImplementedError
