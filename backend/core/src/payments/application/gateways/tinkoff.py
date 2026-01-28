import copy
import json
from decimal import Decimal
from hashlib import sha256

import requests

from payments.application.gateways.interface import PaymentUrlGatewayInterface
from payments.entities.order import OrderProduct


class PaymentUrlGateway(PaymentUrlGatewayInterface):
    def __init__(
        self,
        terminal_key: str,
        password: str,
        taxation: str,
        tax: str,
        delivery_price: int,
        payment_url: str,
    ):
        self.terminal_key = terminal_key
        self.taxation = taxation
        self.password = password
        self.tax = tax
        self.delivery_price = delivery_price
        self.payment_url = payment_url

    def generate_payment_token(self, data: dict) -> str:
        data = copy.deepcopy(data)
        data.pop('DATA', None)
        data.update({'Password': self.password})
        token_data = tuple(str(item) for _, item in sorted(data.items()))
        return sha256(''.join(token_data).encode('utf-8')).hexdigest()

    def generate_receipt(
        self,
        products: list[OrderProduct],
        products_count: dict[str, int],
        customer_phone_number: str,
        with_delivery: bool,
    ) -> dict:
        receipt = {
            'Taxation': self.taxation,
            'Phone': customer_phone_number,
        }
        receipt_items = []
        for product in products:
            item = {}
            item.setdefault('Name', product.title)
            item.setdefault('Quantity', products_count[product.id])
            item.setdefault('Price', int(product.price))
            item.setdefault(
                'Amount', int(product.price) * 100 * int(products_count[product.id]),
            )
            item.setdefault('Tax', self.tax)
            receipt_items.append(item)
        if with_delivery:
            delivery_price = self.delivery_price
            receipt_items.append(
                {
                    'Name': 'Доставка',
                    'Quantity': '1',
                    'Price': delivery_price,
                    'Amount': delivery_price * 100,
                    'Tax': self.tax,
                },
            )
        receipt.update({'Items': receipt_items})
        return receipt

    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        customer_phone_number: str,
        products: list[OrderProduct],
        products_count: dict[str, int],
        with_delivery: bool,
        discount_coefficient: Decimal,
        customer_email: str | None = None,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        data = {
            'TerminalKey': self.terminal_key,
            'Amount': int(amount) * 100,
            'OrderId': str(order_uuid),
            'DATA': {'Phone': customer_phone_number},
        }
        token = self.generate_payment_token(data)
        data.setdefault('Token', token)
        receipt = self.generate_receipt(
            products=products,
            products_count=products_count,
            customer_phone_number=customer_phone_number,
            with_delivery=with_delivery,
        )
        data.setdefault('Receipt', receipt)
        data = json.dumps(data)
        response = requests.post(
            url=self.payment_url,
            headers=headers,
            data=data,
        )
        if response.status_code == 200:
            response = response.json()
            if not response.get('Success'):
                return None
        else:
            return None
        return response.get('PaymentURL')
