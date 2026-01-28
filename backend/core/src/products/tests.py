from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from products.application.serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
)
from products.db.models import Product


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def test_products():
    mock_image = Image.new('RGB', (100, 100))
    image_io = BytesIO()
    mock_image.save(image_io, format='JPEG')
    mock_image_file = ContentFile(image_io.getvalue(), name='mock.jpg')

    products = [
        Product.objects.create(
            title='product1',
            slug='product1',
            image=mock_image_file,
            price=100,
            kind=None,
        ),
        Product.objects.create(
            title='product2',
            slug='product2',
            image=mock_image_file,
            price=200,
            kind=None,
        ),
    ]

    yield products

    for file_path in Path().glob('media/images/mock*.jpg'):
        Path(file_path).unlink()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'slug,session_type',
    [
        ('product1', 'cart'),
        ('product2', 'cart'),
        ('product1', 'favourites'),
        ('product2', 'favourites'),
    ],
)
def test_add_to_session(api_client, slug, session_type):
    """Test adding products to cart and favourites sessions"""

    response = api_client.post(
        reverse('products:api-add-to-session', kwargs={'slug': slug}),
        {'type': session_type},
    )

    session_key = 'cart_products' if session_type == 'cart' else 'favourites'
    assert slug in api_client.session.get(session_key)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'slug,session_type',
    [
        ('product1', 'cart'),
        ('product2', 'cart'),
        ('product1', 'favourites'),
        ('product2', 'favourites'),
    ],
)
def test_delete_from_session(api_client, slug, session_type):
    """Test deleting products from cart and favourites sessions"""

    api_client.post(
        reverse('products:api-add-to-session', kwargs={'slug': slug}),
        {'type': session_type},
    )

    response = api_client.post(
        reverse('products:api-add-to-session', kwargs={'slug': slug}),
        {'type': session_type},
    )

    session_key = 'cart_products' if session_type == 'cart' else 'favourites'
    assert slug not in api_client.session.get(session_key, [])
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
@pytest.mark.parametrize('add_products', [True, False])
def test_check_cart(api_client, add_products):
    """Test cart with and without products"""
    from products.application.serializers import ProductListSerializer

    if add_products:
        for slug in ['product1', 'product2']:
            api_client.post(
                reverse('products:api-add-to-session', kwargs={'slug': slug}),
                {'type': 'cart'},
            )

    response = api_client.get(reverse('products:api-cart-product-list'))

    assert response.status_code == status.HTTP_200_OK

    if not add_products:
        assert response.json() == []
    else:
        from products.db.models import Product

        serializer = ProductListSerializer(
            Product.objects.filter(slug__in=['product1', 'product2']),
            many=True,
            context={'request': response.wsgi_request},
        )
        assert response.json() == serializer.data


@pytest.mark.django_db()
@pytest.mark.parametrize('deactivate_first', [True, False])
def test_check_product_list(api_client, deactivate_first):
    """Test product list with active and inactive products"""

    if deactivate_first:
        test_products[0].is_active = False
        test_products[0].save()
        expected_queryset = Product.objects.active()
    else:
        expected_queryset = Product.objects.all()

    response = api_client.get(reverse('products:api-product-list'))

    serializer = ProductListSerializer(
        expected_queryset,
        many=True,
        context={'request': response.wsgi_request},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('result') == serializer.data


@pytest.mark.django_db()
@pytest.mark.parametrize('slug', ['product1', 'product2'])
def test_check_product_detail(api_client, slug):
    """Test product detail view for different products"""

    response = api_client.get(
        reverse('products:api-product-detail', kwargs={'slug': slug}),
    )

    serializer = ProductDetailSerializer(
        Product.objects.get(slug=slug),
        context={'request': response.wsgi_request},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('result') == serializer.data


@pytest.mark.django_db()
@pytest.mark.parametrize('add_to_favourites', [True, False])
def test_check_favourite_list(api_client, add_to_favourites):
    """Test favourites list with and without products"""

    if add_to_favourites:
        for slug in ['product1', 'product2']:
            api_client.post(
                reverse('products:api-add-to-session', kwargs={'slug': slug}),
                {'type': 'favourites'},
            )

    response = api_client.get(reverse('products:api-favourite-list'))

    assert response.status_code == status.HTTP_200_OK

    if not add_to_favourites:
        assert list(response.data['result']) == []
    else:
        assert len(response.data['result']) > 0
