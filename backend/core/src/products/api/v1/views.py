from config.container import Container
from dependency_injector.wiring import Provide, inject
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from products.interfaces.cart import CartServiceInterface
from products.mixins import FilterQueryMixin, ProductResponseMixin
from products.models import Category, Product
from products.serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


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

    def get_queryset(self) -> QuerySet:
        favourite_products_slug = self.request.session.get('favourites')
        if favourite_products_slug:
            return super().get_queryset().filter(slug__in=[*favourite_products_slug])
        return self.queryset.none()


class CartAPIView(APIView):
    @inject
    def get(
        self,
        request,
        cart_service: CartServiceInterface = Provide[Container.cart_service],
    ) -> Response:
        data = cart_service.get(request)
        return Response(data, status=status.HTTP_200_OK)


class AddToSessionAPIView(APIView):
    @inject
    def post(
        self,
        request,
        slug: str,
        cart_service: CartServiceInterface = Provide[Container.cart_service],
    ) -> Response:
        code = cart_service.add(request, slug)
        if code == 201:
            return Response(status=status.HTTP_201_CREATED)
        elif code == 204:
            return Response(status=status.HTTP_204_NO_CONTENT)
