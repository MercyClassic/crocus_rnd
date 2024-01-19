from typing import List

from accounts.schemas import UserData
from payments.models import Order, OrderProduct
from payments.schemas import OrderData
from products.models import Product


class PaymentRepository:
    def create_order(
        self,
        amount: int,
        data: OrderData,
        user_account: UserData,
    ) -> Order:
        order = Order.objects.create(
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
        )
        return order

    def get_order_products(
        self,
        products_slug: List[str],
    ) -> List[Product]:
        order_products = Product.objects.only('title', 'slug', 'price').filter(
            slug__in=[*products_slug],
        )
        return order_products

    def create_order_products(
        self,
        order_id: int,
        order_products: List[Product],
        products_with_count: dict,
    ) -> None:
        products_to_bulk_create = [
            OrderProduct(
                order_id=order_id,
                product=product,
                count=int(products_with_count.get(product.slug)),
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

    def delete_order(self, uuid: str):
        Order.objects.filter(uuid=uuid).delete()

    def set_is_paid_to_order(self, order: Order) -> None:
        order.is_paid = True
        order.save()
