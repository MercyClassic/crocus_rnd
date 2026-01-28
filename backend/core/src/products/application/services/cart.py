from abc import ABC, abstractmethod
from contextlib import suppress
from typing import Literal

from rest_framework.request import Request

from products.application.serializers import ProductListSerializer
from products.db.models.product import Product


class CartServiceInterface(ABC):
    @abstractmethod
    def add(self, request: Request, product_slug: str) -> Literal[201, 204]:
        raise NotImplementedError

    @abstractmethod
    def get(self, request: Request) -> dict:
        raise NotImplementedError


class CartService(CartServiceInterface):
    def add(self, request: Request, product_slug: str) -> Literal[201, 204]:
        add_to = (
            'cart_products' if request.data.get('type') == 'cart' else 'favourites'
        )

        products = request.session.get(add_to)
        if not isinstance(products, list):
            products = request.session.setdefault(add_to, [])

        if product_slug not in products:
            request.session.get(add_to).append(product_slug)
            request.session.modified = True
            return 201
        else:
            with suppress(ValueError):
                request.session.get(add_to).remove(product_slug)
            request.session.modified = True
            return 204

    def get(self, request: Request) -> dict:
        cart_products = request.session.get('cart_products')
        if cart_products:
            cart_products = Product.objects.filter(slug__in=[*cart_products])
        serializer = ProductListSerializer(
            cart_products,
            many=True,
            context={'request': request},
        )
        return serializer.data
