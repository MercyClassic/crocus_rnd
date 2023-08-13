import asyncio
import copy
import json
import logging
import os
from datetime import datetime
from hashlib import sha256

import requests
from django.db.models import QuerySet

from accounts.models import Account
from bot.handlers.notifications import send_notification_about_new_order
from payments.models import Order, OrderProduct
from payments.serializers import PaymentCreateSerializer
from products.models import Product

logger = logging.getLogger('payment')


class PaymentCreateService:
    def __init__(self, serialized_data: dict):
        for key in PaymentCreateSerializer._declared_fields.keys():
            setattr(self, key, serialized_data.get(key))
        if not self.delivering:
            self.delivery_address = None
            self.delivery_time = None

    @staticmethod
    def generate_payment_token(data: dict) -> str:
        data = copy.deepcopy(data)
        data.pop('DATA', None)
        data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
        token_data = tuple(map(lambda tup: str(tup[1]), sorted(data.items())))
        return sha256(''.join(token_data).encode('utf-8')).hexdigest()

    def generate_receipt(
            self,
            products: QuerySet,
            with_delivery: bool = False,
    ) -> dict:
        customer_phone_number = self.customer_phone_number
        if customer_phone_number[0] != '+':
            customer_phone_number = f'+{self.customer_phone_number}'
        receipt = {
            'Taxation': os.getenv('TINKOFF_TAXATION'),
            'Phone': customer_phone_number,
        }
        request_items = self.items
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
                    'Amount': delivery_price * 100 * 1,
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
            'DATA': {'Phone': self.customer_phone_number},
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

    def get_or_create_customer(self) -> Account:
        try:
            user_account = Account.objects.only('id').get(phone_number=self.customer_phone_number)
        except Account.DoesNotExist:
            user_account = Account.objects.create(
                phone_number=self.customer_phone_number,
                name=self.customer_name,
            )
        return user_account

    def create_order(
            self,
            user_account: Account,
            amount: int,
    ):
        order = Order.objects.create(
            user=user_account,
            amount=amount,
            without_calling=self.without_calling,
            receiver_name=self.receiver_name,
            receiver_phone_number=self.receiver_phone_number,
            delivery_address=self.delivery_address,
            delivery_date=self.delivery_date,
            delivery_time=self.delivery_time,
            note=self.note,
            cash=self.cash,
            is_paid=False,
            delivering=self.delivering,
        )
        return order

    def create_order_products(
            self,
            order: Order,
            order_products: QuerySet,
    ) -> None:
        products_to_bulk_create = []
        for product in order_products:
            products_to_bulk_create.append(OrderProduct(
                order=order,
                product=product,
                count=int(self.items.get(product.slug)),
            ))
        OrderProduct.objects.bulk_create(products_to_bulk_create)

    def create_payment(self) -> str | bool:
        if (
                (self.delivery_date.date() < datetime.utcnow().date())
                or (self.amount > 50350)
                or (any(int(count) < 1 for count in self.items.values()))
        ):
            return False
        order_products = (
            Product.objects
            .only('title', 'slug', 'price')
            .filter(slug__in=[*self.items.keys()])
        )
        if len(order_products) == 0:
            return False
        calculated_amount = sum(
            product.price * int(self.items.get(product.slug)) for product in order_products
        )
        if self.delivering:
            calculated_amount += 350
        if calculated_amount != self.amount:
            return False

        user_account = self.get_or_create_customer()

        order = self.create_order(
            user_account=user_account,
            amount=calculated_amount,
        )

        self.create_order_products(
            order=order,
            order_products=order_products,
        )

        if self.cash:
            asyncio.run(send_notification_about_new_order(order.id))
            return 'OK'

        payment_url = self.get_payment_url(
            order_uuid=str(order.uuid),
            amount=calculated_amount,
            receipt=self.generate_receipt(order_products, self.delivering),
        )
        return payment_url
