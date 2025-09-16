import os
from decimal import Decimal

from accounts.repositories import UserRepository
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from notification_bus.services.sender import NotificationBus
from payments.application.repositories.yookassa import PaymentUrlGateway
from payments.application.services.call_me import CallMeService
from payments.application.services.payment_accept.yookassa import (
    PaymentAcceptService,
)
from payments.application.services.payment_create import PaymentCreateService
from payments.infrastructure.db.repositories.order import PaymentRepository
from products.services.cart import CartService


class Container(DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)
    payment_repo = providers.Factory(PaymentRepository)
    notification_bus = providers.Factory(
        NotificationBus,
        broker_host_uri=os.environ['RABBITMQ_URI'],
    )
    payment_url_gateway = providers.Factory(
        PaymentUrlGateway,
        delivery_price=Decimal(os.environ['DELIVERY_PRICE']),
    )

    payment_create_service = providers.Factory(
        PaymentCreateService,
        user_repo=user_repo,
        payment_repo=payment_repo,
        notification_bus=notification_bus,
        payment_url_gateway=payment_url_gateway,
        delivery_price=Decimal(os.environ['DELIVERY_PRICE']),
    )
    payment_accept_service = providers.Factory(
        PaymentAcceptService,
        payment_repo=payment_repo,
    )
    call_me_service = providers.Factory(
        CallMeService,
        notification_bus=notification_bus,
    )
    cart_service = providers.Factory(
        CartService,
    )


container = Container()
