import re
from datetime import datetime
from typing import Iterable

from django.db import transaction

from accounts.repositories import UserRepository
from payments.application.interfaces.services.payment_create import PaymentCreateServiceInterface
from payments.infrastructure.db.interfaces.repositories.order import PaymentRepositoryInterface
from payments.application.models.order import OrderDTO
from notification_bus.interfaces.sender import NotificationBusInterface
from payments.infrastructure.db.interfaces.repositories.tinkoff import PaymentUrlGatewayInterface
from products.models import Product


class PaymentCreateService(PaymentCreateServiceInterface):
    def __init__(
        self,
            payment_repo: PaymentRepositoryInterface,
            user_repo: UserRepository,
            notification_bus: NotificationBusInterface,
            payment_url_gateway: PaymentUrlGatewayInterface,
    ):
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.notification_bus = notification_bus
        self.payment_url_gateway = payment_url_gateway

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
            amount: int,
            delivering: bool,
    ) -> bool:
        if delivery_date.date() < datetime.utcnow().date():
            return False
        if amount > 50350:
            return False
        if any(int(count) < 1 for count in products_count.values()):
            return False
        if not order_products:
            return False

        if delivering:
            calculated_amount += 350
        if calculated_amount != amount:
            return False
        return True

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
        order_data = OrderDTO(
            products=products,
            amount=amount,
            customer_name=customer_name,
            customer_email=customer_email,
            receiver_name=receiver_name,
            customer_phone_number=self.normalize_phone_number(customer_phone_number),
            receiver_phone_number=self.normalize_phone_number(receiver_phone_number),
            without_calling=without_calling,
            delivery_address=delivery_address,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            note=note,
            cash=cash,
            delivering=delivering,
        )

        order_products = self.payment_repo.get_order_products(order_data.products.keys())

        calculated_amount = sum(
            product.price * int(order_data.products.get(product.slug))
            for product in order_products
        )

        is_permitted = self.check_permissions(
            delivery_date=order_data.delivery_date,
            order_products=order_products,
            products_count=order_data.products,
            calculated_amount=calculated_amount,
            amount=order_data.amount,
            delivering=order_data.delivering,
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
            payment_url = self.payment_url_gateway.get_payment_url(
                order_uuid=str(order.uuid),
                amount=calculated_amount,
                products=order_products,
                products_count=order_data.products,
                with_delivery=order_data.delivering,
                customer_phone_number=order_data.customer_phone_number,
            )
            return payment_url
