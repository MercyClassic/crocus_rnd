from datetime import datetime
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

from PIL import Image
from config.container import container
from django.core.cache import cache
from django.core.files.base import ContentFile
from products.models import Product
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

payment_url_gateway_mock = Mock()
payment_url_gateway_mock.get_payment_url.return_value = 'OK'
container.payment_url_gateway.override(payment_url_gateway_mock)

notification_bus_mock = Mock()
notification_bus_mock.send_order_notification.return_value = None
notification_bus_mock.send_call_me_request_notification.return_value = None
container.notification_bus.override(notification_bus_mock)

call_me_service_mock = Mock()
call_me_service_mock.create_call_me_request.return_value = True
container.call_me_service.override(call_me_service_mock)


class PaymentTests(APITestCase):
    def setUp(self) -> None:
        mock_image = Image.new('RGB', (100, 100))
        image_io = BytesIO()
        mock_image.save(image_io, format='JPEG')
        mock_image_file = ContentFile(image_io.getvalue(), name='mock.jpg')

        Product.objects.create(
            title='product1',
            slug='product1',
            image=mock_image_file,
            price=100,
            kind=None,
        )
        Product.objects.create(
            title='product2',
            slug='product2',
            image=mock_image_file,
            price=200,
            kind=None,
        )

    def tearDown(self) -> None:
        for file_path in Path().glob('media/images/mock*.jpg'):
            Path(file_path).unlink()

    def test_create_payment(self):  # noqa: PLR0915
        payment_create_url = reverse('payments:api-payment-create')
        """ ALL DATA IS VALID """
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
            payment_create_url,
            data=data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ALL DATA IS VALID BUT TIMEOUT"""
        response = self.client.post(
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
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
            payment_create_url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cache.clear()

    def test_call_me(self):
        """PHONE NUMBER IS NOT VALID"""
        call_me_url = reverse('payments:api-call-me')
        response = self.client.post(
            call_me_url,
            {'phone_number': '+19999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        """ PHONE NUMBER IS VALID """
        response = self.client.post(
            call_me_url,
            {'phone_number': '+79999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """ PHONE NUMBER IS VALID BUT TIMEOUT """
        response = self.client.post(
            call_me_url,
            {'phone_number': '+79999999999'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
