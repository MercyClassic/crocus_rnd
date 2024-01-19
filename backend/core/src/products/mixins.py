from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class ProductResponseMixin(GenericAPIView):
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        if kwargs.get(self.lookup_field):
            serializer = self.get_serializer(self.get_object())
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'result': serializer.data,
                'cart_products': request.session.get('cart_products', []),
                'favourites': request.session.get('favourites', []),
            },
        )


class FilterQueryMixin:
    queryset: QuerySet
    request: Request

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.all()
        search = self.request.GET.get('search')
        product_type = self.request.GET.get('type')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search),
            )
        if product_type:
            queryset = queryset.filter(kind=product_type)
        if category:
            queryset = queryset.filter(categories__name=category, categories__is_active=True)
        return queryset
