from collections.abc import Iterable

from accounts.schemas import UserDTO
from products.models import Product

from payments.application.dto.order import OrderDTO
from payments.infrastructure.db.interfaces.repositories.order import (
    PaymentRepositoryInterface,
)
from payments.infrastructure.db.models import Order, OrderProduct, PromoCode


class PaymentRepository(PaymentRepositoryInterface):
    def create_order(
        self,
        amount: int,
        data: OrderDTO,
        user_account: UserDTO,
        promo_code: PromoCode | None,
    ) -> Order:
        return Order.objects.create(
            user_id=user_account.id,
            amount=amount,
            without_calling=data.without_calling,
            customer_email=data.customer_email,
            receiver_name=data.receiver_name,
            receiver_phone_number=data.receiver_phone_number,
            delivery_address=data.delivery_address,
            delivery_date=data.delivery_date,
            delivery_time=data.delivery_time,
            note=data.note,
            cash=data.cash,
            is_paid=False,
            delivering=data.delivering,
            promo_code=promo_code,
        )

    def get_order_products(
        self,
        products_slug: Iterable[str],
    ) -> Iterable[Product]:
        return Product.objects.only('title', 'slug', 'price').filter(
            slug__in=[*products_slug],
        )

    def create_order_products(
        self,
        order_id: int,
        order_products: Iterable[Product],
        products_count: dict[str, int],
    ) -> None:
        products_to_bulk_create = [
            OrderProduct(
                order_id=order_id,
                product=product,
                count=int(products_count.get(product.slug)),
            )
            for product in order_products
        ]
        OrderProduct.objects.bulk_create(products_to_bulk_create)

    def get_order_by_uuid(self, uuid: str) -> Order | None:
        try:
            order = Order.objects.only('id', 'is_paid').get(uuid=uuid)
        except Order.DoesNotExist:
            return None
        return order

    def get_promo_code(self, promo_code: str) -> PromoCode | None:
        try:
            promo_code = PromoCode.objects.get(code=promo_code, is_active=True)
        except PromoCode.DoesNotExist:
            return None
        return promo_code

    def delete_order(self, uuid: str) -> None:
        Order.objects.filter(uuid=uuid).delete()

    def set_is_paid_to_order(self, order: Order) -> None:
        order.is_paid = True
        order.save()
