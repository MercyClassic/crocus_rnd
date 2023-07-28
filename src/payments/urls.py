from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    path('create_payment/', views.CreatePaymentAPIView.as_view(), name='api-payment-create'),
    path('accept_payment/', views.AcceptPaymentAPIView.as_view(), name='api-payment-accept'),
    path('call_me/', views.CallMeAPIView.as_view(), name='call_me'),
]
