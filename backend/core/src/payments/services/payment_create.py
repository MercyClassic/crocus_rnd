import asyncio
import copy
import json
import os
import re
from datetime import datetime
from hashlib import sha256
from typing import List

import requests
from bot.handlers.notifications import send_notification_about_new_order

from accounts.repositories import UserRepository
from payments.repositories import PaymentRepository
from payments.schemas import OrderData
from products.models import Product


class PaymentCreateService:
    def __init__(
        self,
        serialized_data: dict,
        payment_repo: PaymentRepository,
        user_repo: UserRepository,
    ):
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.order_data = OrderData(
            customer_phone_number=self.normalize_phone_number(
                serialized_data.pop('customer_phone_number'),
            ),
            receiver_phone_number=self.normalize_phone_number(
                serialized_data.pop('receiver_phone_number', None),
            ),
            products=serialized_data.pop('items'),
            **serialized_data,
        )

    @staticmethod
    def normalize_phone_number(phone_number: str) -> str:
        phone_number = re.sub(r'[() -]*', '', phone_number)

        if phone_number[0] != '+':
            phone_number = f'+{phone_number}'

        return f'+7{phone_number[2:]}'

    @staticmethod
    def generate_payment_token(data: dict) -> str:
        data = copy.deepcopy(data)
        data.pop('DATA', None)
        data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
        token_data = tuple(map(lambda tup: str(tup[1]), sorted(data.items())))
        return sha256(''.join(token_data).encode('utf-8')).hexdigest()

    def generate_receipt(
        self,
        products: List[Product],
        with_delivery: bool = False,
    ) -> dict:
        receipt = {
            'Taxation': os.getenv('TINKOFF_TAXATION'),
            'Phone': self.order_data.customer_phone_number,
        }
        request_items = self.order_data.products
        receipt_items = []
        for product in products:
            item = {}
            item.setdefault('Name', product.title)
            item.setdefault('Quantity', request_items[product.slug])
            item.setdefault('Price', product.price)
            item.setdefault('Amount', product.price * 100 * int(request_items[product.slug]))
            item.setdefault('Tax', os.getenv('TINKOFF_TAX'))
            receipt_items.append(item)
        if with_delivery:
            delivery_price = int(os.getenv('DELIVERY_PRICE'))
            receipt_items.append(
                {
                    'Name': 'Доставка',
                    'Quantity': '1',
                    'Price': delivery_price,
                    'Amount': delivery_price * 100,
                    'Tax': os.getenv('TINKOFF_TAX'),
                },
            )
        receipt.update({'Items': receipt_items})
        return receipt

    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        receipt: dict,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        data = {
            'TerminalKey': os.getenv('TINKOFF_TERMINAL_KEY'),
            'Amount': int(amount) * 100,
            'OrderId': order_uuid,
            'DATA': {'Phone': self.order_data.customer_phone_number},
        }
        token = self.generate_payment_token(data)
        data.setdefault('Token', token)
        data.setdefault('Receipt', receipt)
        data = json.dumps(data)
        response = requests.post(
            url=os.getenv('TINKOFF_PAYMENT_URL'),
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

    def create_payment(self) -> str | bool:
        if (
            (self.order_data.delivery_date.date() < datetime.utcnow().date())
            or (self.order_data.amount > 50350)
            or (any(int(count) < 1 for count in self.order_data.products.values()))
        ):
            return False
        order_products = self.payment_repo.get_order_products_from_db(
            self.order_data.products.keys(),
        )
        if not order_products:
            return False

        calculated_amount = sum(
            product.price * int(self.order_data.products.get(product.slug))
            for product in order_products
        )

        if self.order_data.delivering:
            calculated_amount += 350
        if calculated_amount != self.order_data.amount:
            return False

        user_account = self.user_repo.get_or_create_customer(
            self.order_data.customer_phone_number,
            self.order_data.customer_name,
        )

        order = self.payment_repo.create_order(
            amount=calculated_amount,
            data=self.order_data,
            user_account=user_account,
        )

        self.payment_repo.create_order_products(
            order_id=order.pk,
            order_products=order_products,
            products_with_count=self.order_data.products,
        )

        if self.order_data.cash:
            asyncio.run(send_notification_about_new_order(order.pk))
            return 'OK'

        payment_url = self.get_payment_url(
            order_uuid=str(order.uuid),
            amount=calculated_amount,
            receipt=self.generate_receipt(order_products, self.order_data.delivering),
        )
        return payment_url
