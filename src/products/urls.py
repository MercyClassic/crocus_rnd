from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('flower/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('favourites/', views.FavouriteView.as_view(), name='favourite-list'),
    path('cart/', views.CartView.as_view(), name='api-cart-product-list'),
    path('add_to_session/<slug:slug>/', views.AddToSessionAPIView.as_view(), name='add-to-session'),
    path('about_shop/', views.about_shop, name='about_shop'),
    path('contact_information/', views.contact_information, name='contact_information'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]
