from django.shortcuts import render
from django.views import generic
from rest_framework.views import APIView

from .mixins import CountCartProductsMixin, FilterQueryMixin
from .models import Product
from .services import cart_service


class ProductListView(FilterQueryMixin, CountCartProductsMixin, generic.ListView):
    queryset = Product.objects.active().order_by('-id')
    template_name = 'products/home.html'
    context_object_name = 'products'


class ProductDetailView(CountCartProductsMixin, generic.DetailView):
    queryset = Product.objects.active().prefetch_related('images')
    template_name = 'products/product-detail.html'
    context_object_name = 'product'


class FavouriteView(FilterQueryMixin, CountCartProductsMixin, generic.ListView):
    queryset = Product.objects.active()
    template_name = 'products/favourites.html'
    context_object_name = 'products'

    def get_queryset(self):
        favourites_slug = self.request.session.get('favourites')
        if favourites_slug:
            return super().get_queryset(self.request).filter(slug__in=[*favourites_slug])
        return self.queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('ip', self.request.META)
        return context


class CartView(APIView):
    def get(self, request, *args, **kwargs):
        response = cart_service.get_cart(request)
        return response


class AddToSessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        response = cart_service.add_to_cart(request, **kwargs)
        return response


def about_shop(request):
    return render(request, 'products/about_shop.html')


def contact_information(request):
    return render(request, 'products/contact_information.html')


def privacy_policy(request):
    return render(request, 'products/privacy_policy.html')
