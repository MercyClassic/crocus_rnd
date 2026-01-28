from django.db.models import Prefetch

from payments.db.models import (
    Order as OrderModel,
)
from payments.db.models import (
    OrderProduct as OrderProductModel,
)
from payments.db.models import (
    PromoCode as PromoCodeModel,
)
from payments.domain.entities.order import Order, OrderProduct, PromoCode
from payments.domain.entities.order_id import OrderId
from payments.domain.entities.value_objects import Money


class OrderRepository:
    def __init__(self, delivery_price: Money):
        self._delivery_price = delivery_price

    def map(self, order_model: OrderModel) -> Order:
        order_id = OrderId(order_model.uuid)

        promo_code = (
            PromoCode(
                id=order_model.promo_code.id,
                code=order_model.promo_code.code,
                value=order_model.promo_code.value,
                is_percent=order_model.promo_code.is_percent,
                is_active=order_model.promo_code.is_active,
            )
            if order_model.promo_code
            else None
        )

        products = [
            OrderProduct(
                id=order_product.product.id,
                slug=order_product.product.slug,
                count=order_product.count,
                title=order_product.product.title,
                price=Money(order_product.product.price),
            )
            for order_product in order_model.order_products.all()
        ]

        return Order(
            id=order_id,
            user_id=order_model.user_id,
            amount=order_model.amount,
            delivering=order_model.delivering,
            without_calling=order_model.without_calling,
            customer_email=order_model.customer_email,
            receiver_name=order_model.receiver_name,
            receiver_phone_number=order_model.receiver_phone_number,
            delivery_address=order_model.delivery_address,
            delivery_date=order_model.delivery_date,
            delivery_time=order_model.delivery_time,
            note=order_model.note,
            cash=order_model.cash,
            is_paid=order_model.is_paid,
            products=products,
            products_count={
                order_product.product.slug: order_product.count
                for order_product in order_model.order_products.all()
            },
            promo_code=promo_code,
            delivery_price=self._delivery_price,
        )

    def get(self, order_id: OrderId) -> Order | None:
        try:
            return self.map(
                OrderModel.objects.select_related('promo_code')
                .prefetch_related(
                    Prefetch(
                        'order_products',
                        queryset=OrderProductModel.objects.select_related('product'),
                    ),
                )
                .get(uuid=order_id),
            )
        except OrderModel.DoesNotExist:
            return None

    def save(self, order: Order) -> OrderModel:
        order_model = OrderModel.objects.create(
            uuid=order.id,
            user_id=order.user_id,
            amount=order.amount,
            is_paid=order.is_paid,
            delivering=order.delivering,
            without_calling=order.without_calling,
            customer_email=order.customer_email,
            receiver_name=order.receiver_name,
            receiver_phone_number=order.receiver_phone_number,
            delivery_address=order.delivery_address,
            delivery_date=order.delivery_date,
            delivery_time=order.delivery_time,
            note=order.note,
            cash=order.cash,
            promo_code_id=order.promo_code.id if order.promo_code else None,
        )
        if order.products:
            products_to_bulk_create = [
                OrderProductModel(
                    order=order_model,
                    product_id=product.id,
                    count=product.count,
                )
                for product in order.products
            ]
            OrderProductModel.objects.bulk_create(products_to_bulk_create)

        return order

    def update(self, order: Order) -> None:
        OrderModel.objects.filter(uuid=order.id).update(
            is_paid=order.is_paid,
            delivering=order.delivering,
            without_calling=order.without_calling,
            customer_email=order.customer_email,
            receiver_name=order.receiver_name,
            receiver_phone_number=order.receiver_phone_number,
            delivery_address=order.delivery_address,
            delivery_date=order.delivery_date,
            delivery_time=order.delivery_time,
            note=order.note,
            cash=order.cash,
        )

    def delete(self, order_id: OrderId) -> None:
        OrderModel.objects.filter(uuid=order_id).delete()


class PromoCodeRepository:
    def get(self, promo_code: str):
        try:
            promo_code = PromoCodeModel.objects.get(code=promo_code, is_active=True)
        except PromoCodeModel.DoesNotExist:
            return None
        return promo_code
