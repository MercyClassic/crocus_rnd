from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import FilterQueryMixin, ProductResponseMixin
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)
from .services import cart_service


class ProductListAPIView(FilterQueryMixin, ProductResponseMixin):
    queryset = Product.objects.active()
    serializer_class = ProductListSerializer


class ProductDetailAPIView(ProductResponseMixin):
    queryset = Product.objects.active().prefetch_related('images')
    serializer_class = ProductDetailSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class FavouriteListAPIView(FilterQueryMixin, ProductResponseMixin):
    queryset = Product.objects.active()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        favourite_products_slug = self.request.session.get('favourites')
        if favourite_products_slug:
            return super().get_queryset().filter(slug__in=[*favourite_products_slug])
        return self.queryset.none()


class CartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = cart_service.get_cart(request)
        return Response(data, status=status.HTTP_200_OK)


class AddToSessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        code = cart_service.add_to_cart(request, **kwargs)
        if code == 201:
            return Response(status=status.HTTP_201_CREATED)
        elif code == 204:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
