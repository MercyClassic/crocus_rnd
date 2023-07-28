from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer


def add_to_cart(
        request: Request,
        **kwargs,
) -> Response:
    if request.data.get('type') == 'cart':
        add_to = 'cart_products'
    else:
        add_to = 'favourites'
    products = request.session.get(add_to)
    if not isinstance(products, list):
        products = request.session.setdefault(add_to, [])
    product = kwargs.get('slug')
    if product not in products:
        request.session.get(add_to).append(product)
        request.session.modified = True
        return Response(status=status.HTTP_201_CREATED)
    else:
        try:
            request.session.get(add_to).remove(product)
            request.session.modified = True
        except ValueError:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_cart(request: Request) -> Response:
    cart_products = request.session.get('cart_products')
    if cart_products:
        cart_products = Product.objects.filter(slug__in=[*cart_products])
    serializer = ProductSerializer(cart_products, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
