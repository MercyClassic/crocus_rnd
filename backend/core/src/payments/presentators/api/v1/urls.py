from django.urls import path

from payments.presentators.api.v1 import views

urlpatterns = [
    path(
        'api/v1/create_payment',
        views.CreatePaymentAPIView.as_view(),
        name='api-payment-create',
    ),
    path(
        'api/v1/accept_payment',
        views.AcceptPaymentAPIView.as_view(),
        name='api-payment-accept',
    ),
    path(
        'api/v1/call_me',
        views.CallMeAPIView.as_view(),
        name='api-call-me',
    ),
]
