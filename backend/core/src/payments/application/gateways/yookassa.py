import logging
import os
import uuid
from decimal import Decimal

from yookassa import Configuration, Payment

from payments.application.gateways.interface import PaymentUrlGatewayInterface
from payments.domain.entities.order import OrderProduct
from payments.domain.entities.order_id import OrderId

logger = logging.getLogger(__name__)

Configuration.account_id = os.environ['YOOKASSA_ACCOUNT_ID']
Configuration.secret_key = os.environ['YOOKASSA_SECRET_KEY']


class PaymentUrlGateway(PaymentUrlGatewayInterface):
    def __init__(self, delivery_price: int):
        self.delivery_price = delivery_price

    def generate_receipt(
        self,
        products: list[OrderProduct],
        products_count: dict[str, int],
        customer_phone_number: str,
        customer_email: str,
        with_delivery: bool,
        discount_coefficient: Decimal,
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
                        'value': product.total_price * Decimal(discount_coefficient),
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
                },
            )
        return receipt

    def get_payment_url(
        self,
        order_id: OrderId,
        amount: int,
        customer_phone_number: str,
        products: list[OrderProduct],
        products_count: dict[str, int],
        with_delivery: bool,
        customer_email: str | None,
        discount_coefficient: Decimal,
    ) -> str | None:
        data = {
            'amount': {
                'value': amount,
                'currency': 'RUB',
            },
            'metadata': {'order_id': str(order_id)},
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
                discount_coefficient,
            )
        payment = Payment.create(data, uuid.uuid4())
        if payment.status == 'pending':
            logger.info(f'Создан заказ. Входные данные: {payment.json()}')
            return payment.confirmation.confirmation_url
        else:
            logger.warning(f'Заказ не создан. Входные данные: {payment.json()}')
