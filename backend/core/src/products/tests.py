from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from products.models import Product
from products.serializers import ProductDetailSerializer, ProductListSerializer


class ProductTests(APITestCase):
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

    def test_add_to_session(self):
        """ADD FIRST PRODUCT TO CART"""
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product1'}),
            {
                'type': 'cart',
            },
        )
        self.assertIn('product1', self.client.session.get('cart_products'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ ADD SECOND PRODUCT TO CART """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product2'}),
            {
                'type': 'cart',
            },
        )
        self.assertIn('product2', self.client.session.get('cart_products'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ ADD FIRST PRODUCT TO FAVOURITES """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product1'}),
            {
                'type': 'favourites',
            },
        )
        self.assertIn('product1', self.client.session.get('favourites'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ ADD SECOND PRODUCT TO FAVOURITES """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product2'}),
            {
                'type': 'favourites',
            },
        )
        self.assertIn('product2', self.client.session.get('favourites'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_from_session(self):
        self.test_add_to_session()
        """ DELETE FIRST PRODUCT FROM CART """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product1'}),
            {
                'type': 'cart',
            },
        )
        self.assertNotIn('product1', self.client.session.get('cart_products'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        """ DELETE SECOND PRODUCT FROM CART """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product2'}),
            {
                'type': 'cart',
            },
        )
        self.assertNotIn('product2', self.client.session.get('cart_products'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        """ DELETE FIRST PRODUCT FROM FAVOURITES """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product1'}),
            {
                'type': 'favourites',
            },
        )
        self.assertNotIn('product1', self.client.session.get('favourites'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        """ DELETE SECOND PRODUCT FROM FAVOURITES """
        response = self.client.post(
            reverse('api-add-to-session', kwargs={'slug': 'product2'}),
            {
                'type': 'favourites',
            },
        )
        self.assertNotIn('product2', self.client.session.get('favourites'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_check_cart(self):
        """CHECK WITH NO PRODUCTS IN CART"""
        response = self.client.get(reverse('api-cart-product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])
        """ CHECK WITH PRODUCTS IN CART """
        self.test_add_to_session()
        response = self.client.get(reverse('api-cart-product-list'))
        serializer = ProductListSerializer(
            Product.objects.filter(slug__in=['product1', 'product2']),
            many=True,
            context={'request': response.wsgi_request},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_check_product_list(self):
        """CHECK ACTIVE PRODUCTS"""
        response = self.client.get(reverse('api-product-list'))
        serializer = ProductListSerializer(
            Product.objects.all(),
            many=True,
            context={'request': response.wsgi_request},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('result'), serializer.data)

        product = Product.objects.first()
        product.is_active = False
        product.save()

        response = self.client.get(reverse('api-product-list'))
        serializer = ProductListSerializer(
            Product.objects.active(),
            many=True,
            context={'request': response.wsgi_request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('result'), serializer.data)

    def test_check_product_detail(self):
        response = self.client.get(
            reverse('api-product-detail', kwargs={'slug': 'product1'}),
        )
        serializer = ProductDetailSerializer(
            Product.objects.get(slug='product1'),
            context={'request': response.wsgi_request},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('result'), serializer.data)

    def test_check_favourite_list(self):
        """CHECK FAVOURITES IF IT IS NONE"""
        response = self.client.get(reverse('api-favourite-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data['result']), [])
        """ CHECK FAVOURITES IF IT IS NOT NONE """
        self.test_add_to_session()
        response = self.client.get(reverse('api-favourite-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
