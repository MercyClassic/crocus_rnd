from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.repositories import UserRepository
from payments.repositories import PaymentRepository
from payments.serializers import PaymentCreateSerializer
from payments.services.payment_create import PaymentCreateService
from products.models import Product


class TestPaymentCreateService(PaymentCreateService):
    def get_payment_url(
        self,
        order_uuid: str,
        amount: int,
        receipt: dict,
    ) -> str:
        data = {
            'TerminalKey': 'TINKOFF_TERMINAL_KEY',
            'Amount': int(amount) * 100,
            'OrderId': order_uuid,
            'DATA': {'Phone': self.order_data.customer_phone_number},
        }
        token = self.generate_payment_token(data)
        data.setdefault('Token', token)
        data.setdefault('Receipt', receipt)
        return 'OK'


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
        payment_service = TestPaymentCreateService(
            serializer.validated_data,
            PaymentRepository(),
            UserRepository(),
        )
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')

        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 650,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_address': 'улица Пушкина',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': True,
            'cash': True,
        }
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service = TestPaymentCreateService(
            serializer.validated_data,
            PaymentRepository(),
            UserRepository(),
        )
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')
        data = {
            'items': {'product1': 2, 'product2': 1},
            'amount': 400,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': False,
            'cash': True,
        }
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service = TestPaymentCreateService(
            serializer.validated_data,
            PaymentRepository(),
            UserRepository(),
        )
        result = payment_service.create_payment()
        self.assertEqual(result, 'OK')
        """ AMOUNT IS NOT VALID """
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 301,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': False,
            'cash': True,
        }
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service = TestPaymentCreateService(
            serializer.validated_data,
            PaymentRepository(),
            UserRepository(),
        )
        result = payment_service.create_payment()
        self.assertEqual(result, False)
        """ NAME IS NOT VALID """
        data = {
            'items': {'product1': 1, 'product2': 1},
            'amount': 300,
            'customer_name': 'i' * 201,
            'customer_phone_number': '+79999999999',
            'without_calling': False,
            'customer_email': '',
            'delivery_time': '',
            'delivery_date': datetime.utcnow(),
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
            'without_calling': False,
            'customer_email': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
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
            'without_calling': False,
            'customer_email': '',
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': False,
            'cash': True,
        }
        serializer = PaymentCreateSerializer(data=data)
        serializer.is_valid()
        payment_service = TestPaymentCreateService(
            serializer.validated_data,
            PaymentRepository(),
            UserRepository(),
        )
        result = payment_service.create_payment()
        self.assertEqual(result, False)
        """ ITEMS CANT BE NULL """
        data = {
            'items': {},
            'amount': 200,
            'customer_name': 'Test Name',
            'customer_phone_number': '+79999999999',
            'without_calling': False,
            'delivery_date': datetime.utcnow(),
            'delivery_time': '',
            'delivering': False,
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
            'without_calling': False,
            'customer_email': '',
            'delivery_date': '',
            'delivery_time': '',
            'delivering': False,
            'cash': True,
        }
        serializer = PaymentCreateSerializer(data=data)
        result = serializer.is_valid()
        self.assertEqual(result, False)

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
