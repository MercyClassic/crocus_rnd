import re
from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal

from accounts.repositories import UserRepository
from django.db import transaction
from notification_bus.interfaces.sender import NotificationBusInterface
from payments.infrastructure.db.models import PromoCode
from products.models import Product

from payments.application.interfaces.services.payment_create import (
    PaymentCreateServiceInterface,
)
from payments.application.models.order import OrderDTO
from payments.infrastructure.db.interfaces.repositories.order import (
    PaymentRepositoryInterface,
)
from payments.application.interfaces.repositories.base import (
    PaymentUrlGatewayInterface,
)


class PaymentCreateService(PaymentCreateServiceInterface):
    def __init__(
        self,
        payment_repo: PaymentRepositoryInterface,
        user_repo: UserRepository,
        notification_bus: NotificationBusInterface,
        payment_url_gateway: PaymentUrlGatewayInterface,
        delivery_price: Decimal,
    ):
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.notification_bus = notification_bus
        self.payment_url_gateway = payment_url_gateway
        self.delivery_price = delivery_price

    def normalize_phone_number(self, phone_number: str) -> str:
        phone_number = re.sub(r'[() -]*', '', phone_number)

        if phone_number[0] != '+':
            phone_number = f'+{phone_number}'

        return f'+7{phone_number[2:]}'

    def check_permissions(
        self,
        delivery_date: datetime,
        order_products: Iterable[Product],
        products_count: dict[str, int],
        calculated_amount: int,
        amount: Decimal,
    ) -> bool:
        if delivery_date.date() < datetime.utcnow().date():
            return False
        if amount > 50000 + self.delivery_price:
            return False
        if any(int(count) < 1 for count in products_count.values()):
            return False
        if not order_products:
            return False

        if calculated_amount != amount:
            return False
        return True

    def get_discount_coefficient(
        self,
        promo_code: PromoCode,
        amount: Decimal | int,
    ) -> Decimal:
        if promo_code:
            return promo_code.get_discount_coefficient(amount)
        return Decimal(1)

    def create_payment(self, order_data: OrderDTO) -> str | bool:
        order_data.customer_phone_number = self.normalize_phone_number(
            order_data.customer_phone_number
        )
        order_data.receiver_phone_number = self.normalize_phone_number(
            order_data.receiver_phone_number
        )

        order_products = self.payment_repo.get_order_products(
            order_data.products.keys()
        )

        calculated_amount = sum(
            product.price * int(order_data.products.get(product.slug))
            for product in order_products
        )

        promo_code = self.payment_repo.get_promo_code(order_data.promo_code)
        discount_coefficient = self.get_discount_coefficient(
            promo_code, calculated_amount
        )

        calculated_amount *= discount_coefficient

        if order_data.delivering:
            calculated_amount += self.delivery_price

        is_permitted = self.check_permissions(
            delivery_date=order_data.delivery_date,
            order_products=order_products,
            products_count=order_data.products,
            calculated_amount=calculated_amount,
            amount=order_data.amount,
        )
        if not is_permitted:
            return False

        user_account = self.user_repo.get_or_create_customer(
            order_data.customer_phone_number,
            order_data.customer_name,
        )
        with transaction.atomic():
            order = self.payment_repo.create_order(
                amount=calculated_amount,
                data=order_data,
                user_account=user_account,
                promo_code=promo_code,
            )

            self.payment_repo.create_order_products(
                order_id=order.pk,
                order_products=order_products,
                products_count=order_data.products,
            )

        self.notification_bus.send_order_notification(order.pk)

        if order_data.cash:
            return 'OK'
        else:
            return self.payment_url_gateway.get_payment_url(
                order_uuid=str(order.uuid),
                amount=calculated_amount,
                products=order_products,
                products_count=order_data.products,
                with_delivery=order_data.delivering,
                customer_phone_number=order_data.customer_phone_number,
                customer_email=order_data.customer_email,
                discount_coefficient=discount_coefficient,
            )
