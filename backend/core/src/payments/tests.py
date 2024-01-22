from datetime import datetime

from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from interfaces.notification_bus import NotificationBusInterface
from interfaces.services.call_me import CallMeServiceInterface
from interfaces.services.payment_create import PaymentCreateServiceInterface
from ioc.ioc import container
from payments.services.call_me import CallMeService
from payments.services.payment_create import PaymentCreateService
from products.models import Product
from rabbitmq.notification_bus import NotificationBus


class PaymentCreateServiceOverride(PaymentCreateService):
    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        receipt: dict,
    ) -> str:
        return 'OK'


class CallMeServiceOverride(CallMeService):
    def create_call_me_request(self, *args, **kwargs) -> bool:
        return True


class NotificationBusOverride(NotificationBus):
    def __init__(self, *args, **kwargs):
        pass

    def __del__(self):
        pass

    def send_order_notification(self, order_id: int) -> None:
        pass

    def send_call_me_request_notification(self, phone_number: str) -> None:
        pass


container.override(PaymentCreateServiceInterface, PaymentCreateServiceOverride)
container.override(CallMeServiceInterface, CallMeServiceOverride)
container.override(NotificationBusInterface, NotificationBusOverride)


class PaymentTests(APITestCase):
    def setUp(self):
        Product.objects.create(
            title='product1',
            slug='product1',
            image='images/test_image.jpg',
            price=100,
            kind=None,
        )
        Product.objects.create(
            title='product2',
            slug='product2',
            image='images/test_image.jpg',
            price=200,
            kind=None,
        )

    def test_create_payment(self):
        """ALL DATA IS VALID"""
        cache.clear()
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 300,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': 'Test Name',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': 'улица Пушкина',
            'delivery_time': '',
            'delivery_date': datetime.utcnow(),
            'note': 'Примечание',
            'cash': True,
            'delivering': False,
        }
        cache.clear()
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ALL DATA IS VALID BUT TIMEOUT"""
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        cache.clear()
        """ALL DATA IS VALID"""
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 650,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': 'улица Пушкина',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': True,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cache.clear()
        """ALL DATA IS VALID"""
        data = {
            'items': {'product1': 2, 'product2': 1},
            'amount': 400,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cache.clear()
        """ AMOUNT IS NOT VALID """
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 301,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()
        """ NAME IS NOT VALID """
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 300,
            'customer_name': 'i' * 201,
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_time': '',
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()
        """ PHONE NUMBER IS NOT VALID """
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 300,
            'customer_name': 'Test Name',
            'customer_phone_number': '42331231',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()
        """ COUNT COULD NOT BE 0 """
        data = {
            'items': {'product1': 0, 'product2': 1},
            'amount': 200,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()
        """ ITEMS CANT BE NULL """
        data = {
            'items': {},
            'amount': 200,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'delivery_address': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': False,
            'note': 'Примечание',
            'customer_email': '',
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()
        """ DELIVERY DATE CANT BE NULL """
        data = {
            'items': {},
            'amount': 200,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'receiver_name': '',
            'receiver_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': '',
            'delivery_date': '',
            'delivery_time': '',
            'note': 'Примечание',
            'delivering': False,
            'cash': True,
        }
        response = self.client.post(
            reverse('api-payment-create'),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()

    def test_call_me(self):
        """PHONE NUMBER IS NOT VALID"""
        response = self.client.post(
            reverse('api-call-me'),
            {'phone_number': '+19999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        """ PHONE NUMBER IS VALID """
        response = self.client.post(
            reverse('api-call-me'),
            {'phone_number': '+79999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """ PHONE NUMBER IS VALID BUT TIMEOUT """
        response = self.client.post(
            reverse('api-call-me'),
            {'phone_number': '+79999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
