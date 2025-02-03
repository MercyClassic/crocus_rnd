import logging
import os
import uuid
from collections.abc import Iterable

from products.models import Product
from yookassa import Configuration, Payment

from payments.application.interfaces.repositories.base import (
    PaymentUrlGatewayInterface,
)

logger = logging.getLogger(__name__)

Configuration.account_id = os.environ['YOOKASSA_ACCOUNT_ID']
Configuration.secret_key = os.environ['YOOKASSA_SECRET_KEY']


class PaymentUrlGateway(PaymentUrlGatewayInterface):
    def __init__(self, delivery_price: int):
        self.delivery_price = delivery_price

    def generate_receipt(
        self,
        products: Iterable[Product],
        products_count: dict[str, int],
        customer_phone_number: str,
        customer_email: str,
        with_delivery: bool,
    ) -> dict:
        receipt = {
            'customer': {
                'email': customer_email,
                'phone_number': customer_phone_number,
            },
            'items': [
                {
                    'description': product.title,
                    'quantity': products_count[product.slug],
                    'amount': {
                        'value': str(
                            float(product.price) * int(products_count[product.slug])
                        ),
                        'currency': 'RUB',
                    },
                    'vat_code': '1',
                    'payment_mode': 'full_prepayment',
                    'payment_subject': 'commodity',
                }
                for product in products
            ],
        }
        if with_delivery:
            receipt['items'].append(
                {
                    'description': 'Доставка',
                    'quantity': '1',
                    'amount': {
                        'value': str(self.delivery_price),
                        'currency': 'RUB',
                    },
                    'vat_code': '1',
                    'payment_mode': 'full_prepayment',
                    'payment_subject': 'service',
                }
            )
        return receipt

    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        customer_phone_number: str,
        products: Iterable[Product],
        products_count: dict[str, int],
        with_delivery: bool,
        customer_email: str | None,
    ) -> str | None:
        data = {
            'amount': {
                'value': amount,
                'currency': 'RUB',
            },
            'metadata': {'order_id': order_uuid},
            'confirmation': {'type': 'redirect', 'return_url': os.environ['DOMAIN']},
            'capture': True,
        }
        if customer_email:
            data['receipt'] = self.generate_receipt(
                products,
                products_count,
                customer_phone_number,
                customer_email,
                with_delivery,
            )
        payment = Payment.create(data, uuid.uuid4())
        if payment.status == 'pending':
            logger.info(f'Создан заказ. Входные данные: {payment.json()}')
            return payment.confirmation.confirmation_url
