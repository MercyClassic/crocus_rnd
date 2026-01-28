import os

import pytest
from datetime import datetime
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock
from PIL import Image
from django.core.cache import cache
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from payments.db.models import PromoCode as PromoCodeModel
from products.db.models import Product as ProductModel


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def mock_container():
    from config.container import container

    payment_url_gateway_mock = Mock()
    payment_url_gateway_mock.get_payment_url.return_value = 'OK'
    container.payment_url_gateway.override(payment_url_gateway_mock)

    notification_bus_mock = Mock()
    notification_bus_mock.order_created.return_value = None
    notification_bus_mock.call_me_requested.return_value = None
    container.notification_bus.override(notification_bus_mock)

    call_me_interactor_mock = Mock()
    call_me_interactor_mock.create_call_me_request.return_value = True
    container.call_me_interactor.override(call_me_interactor_mock)

    yield {
        'payment_gateway': payment_url_gateway_mock,
        'notification_bus': notification_bus_mock,
        'call_me_interactor': call_me_interactor_mock,
    }

    container.payment_url_gateway.reset_override()
    container.notification_bus.reset_override()
    container.call_me_interactor.reset_override()


@pytest.fixture(autouse=True)
def _setup_db_entities():
    mock_image = Image.new('RGB', (100, 100))
    image_io = BytesIO()
    mock_image.save(image_io, format='JPEG')
    mock_image_file = ContentFile(image_io.getvalue(), name='mock.jpg')

    ProductModel.objects.create(
        title='product1',
        slug='product1',
        image=mock_image_file,
        price=100,
        kind=None,
    )
    ProductModel.objects.create(
        title='product2',
        slug='product2',
        image=mock_image_file,
        price=200,
        kind=None,
    )
    PromoCodeModel.objects.create(
        code='some_code', value=100, is_percent=False, is_active=True
    )

    yield

    for file_path in Path().glob('media/images/mock*.jpg'):
        Path(file_path).unlink()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_data,expected_status,cache_clear_before,description',
    [
        (
            {
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
            },
            status.HTTP_201_CREATED,
            True,
            'All data is valid without delivery',
        ),
        (
            {
                'items': {'product1': 1, 'product2': 1},
                'amount': 200,
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
                'promo_code': 'some_code',
            },
            status.HTTP_201_CREATED,
            True,
            'All data is valid with promo_code',
        ),
        (
            {
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
            },
            status.HTTP_403_FORBIDDEN,
            False,
            'All data is valid but timeout',
        ),
        (
            {
                'items': {'product1': 1, 'product2': 1},
                'amount': 300 + int(os.getenv('DELIVERY_PRICE')),
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
            },
            status.HTTP_201_CREATED,
            True,
            'All data is valid with pickup',
        ),
        (
            {
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
            },
            status.HTTP_201_CREATED,
            True,
            'Different quantities of products',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Amount is not valid',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Name is not valid (too long)',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Phone number is not valid',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Count could not be 0',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Items cant be null',
        ),
        (
            {
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
            },
            status.HTTP_400_BAD_REQUEST,
            True,
            'Delivery date cant be null',
        ),
    ],
)
def test_create_payment(
    api_client,
    test_data,
    expected_status,
    cache_clear_before,
    description,
):
    """Test payment creation with various scenarios"""

    if cache_clear_before:
        cache.clear()

    response = api_client.post(
        reverse('payments:api-payment-create'),
        data=test_data,
        format='json',
    )

    assert (
        response.status_code == expected_status
    ), f"Failed for scenario: {description}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    'phone_number,expected_status,cache_clear_before,description',
    [
        (
            '+19999999999',
            status.HTTP_400_BAD_REQUEST,
            True,
            'Phone number is not valid',
        ),
        (
            '+79999999999',
            status.HTTP_200_OK,
            True,
            'Phone number is valid',
        ),
        (
            '+79999999999',
            status.HTTP_403_FORBIDDEN,
            False,
            'Phone number is valid but timeout',
        ),
    ],
)
def test_call_me(
    api_client,
    phone_number,
    expected_status,
    cache_clear_before,
    description,
):
    """Test call me functionality"""

    if cache_clear_before:
        cache.clear()

    response = api_client.post(
        reverse('payments:api-call-me'),
        {'phone_number': phone_number},
    )

    assert (
        response.status_code == expected_status
    ), f"Failed for scenario: {description}"
