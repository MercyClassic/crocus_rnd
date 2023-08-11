from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/v1/flowers',
        views.ProductListAPIView.as_view(),
        name='api-product-list',
    ),
    path(
        'api/v1/flowers/<slug:slug>',
        views.ProductDetailAPIView.as_view(),
        name='api-product-detail',
    ),
    path(
        'api/v1/categories',
        views.CategoryListAPIView.as_view(),
        name='api-category-list',
    ),
    path(
        'api/v1/favourites',
        views.FavouriteView.as_view(),
        name='api-favourite-list',
    ),
    path(
        'api/v1/cart',
        views.CartView.as_view(),
        name='api-cart-product-list',
    ),
    path(
        'api/v1/add_to_session/<slug:slug>',
        views.AddToSessionAPIView.as_view(),
        name='api-add-to-session',
    ),
]
