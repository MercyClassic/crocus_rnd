from typing import Literal

from rest_framework.request import Request

from products.interfaces.cart import CartServiceInterface
from products.models import Product
from products.serializers import ProductListSerializer


class CartService(CartServiceInterface):
    def add_to_cart(self, request: Request, product_slug: str) -> Literal[201, 204]:
        if request.data.get('type') == 'cart':
            add_to = 'cart_products'
        else:
            add_to = 'favourites'

        products = request.session.get(add_to)
        if not isinstance(products, list):
            products = request.session.setdefault(add_to, [])

        if product_slug not in products:
            request.session.get(add_to).append(product_slug)
            request.session.modified = True
            return 201
        else:
            try:
                request.session.get(add_to).remove(product_slug)
            except ValueError:
                pass
            request.session.modified = True
            return 204

    def get_cart(self, request: Request) -> dict:
        cart_products = request.session.get('cart_products')
        if cart_products:
            cart_products = Product.objects.filter(slug__in=[*cart_products])
        serializer = ProductListSerializer(
            cart_products,
            many=True,
            context={'request': request},
        )
        return serializer.data
