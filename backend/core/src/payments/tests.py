from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.repositories import UserRepository
from container import container
from payments.repositories import PaymentRepository
from payments.serializers import PaymentCreateSerializer
from payments.services.payment_create import PaymentCreateService
from products.models import Product


class PaymentCreateServiceOverride(PaymentCreateService):
    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        receipt: dict,
    ) -> str:
        return 'OK'


class CallMeServiceOverride:
    def create_call_me_request(self, *args, **kwargs) -> bool:
        return True


class NotificationBusMock:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send_order_notification(self, order_id: int) -> None:
        pass

    def send_call_me_request_notification(self, phone_number: str) -> None:
        pass


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
        payment_service = PaymentCreateServiceOverride(
            PaymentRepository(),
            UserRepository(),
            NotificationBusMock(),
        )

        """ALL DATA IS VALID"""
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service.fill_in_with_data(serializer.validated_data)
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service.fill_in_with_data(serializer.validated_data)
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service.fill_in_with_data(serializer.validated_data)
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service.fill_in_with_data(serializer.validated_data)
        result = payment_service.create_payment()
        self.assertEqual(result, False)
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
        serializer = PaymentCreateSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)
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
        serializer = PaymentCreateSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service.fill_in_with_data(serializer.validated_data)
        result = payment_service.create_payment()
        self.assertEqual(result, False)
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
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(result, False)
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
        serializer = PaymentCreateSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

    def test_call_me(self):
        container.call_me_service.override(CallMeServiceOverride())

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
