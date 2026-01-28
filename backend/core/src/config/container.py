import os
from decimal import Decimal

from accounts.repositories import UserRepository
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from notification_bus.sender import NotificationBus
from payments.application.gateways.yookassa import PaymentUrlGateway
from payments.application.interactors.call_me import CallMeInteractor
from payments.application.interactors.create_order import CreateOrderInteractor
from payments.application.interactors.payment_accept.yookassa import (
    PaymentAcceptService,
)
from payments.db.repositories.order import (
    OrderRepository,
    PromoCodeRepository,
)
from payments.domain.entities.value_objects import Money
from products.application.services.cart import CartService
from products.db.repositories.product import ProductRepository


class Container(DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)
    order_repo = providers.Factory(
        OrderRepository, delivery_price=Money(os.environ['DELIVERY_PRICE']),
    )
    promo_code_repo = providers.Factory(PromoCodeRepository)
    product_repo = providers.Factory(ProductRepository)
    notification_bus = providers.Factory(
        NotificationBus,
        broker_host_uri=os.environ['RABBITMQ_URI'],
    )
    payment_url_gateway = providers.Factory(
        PaymentUrlGateway,
        delivery_price=Decimal(os.environ['DELIVERY_PRICE']),
    )

    create_order_interactor = providers.Factory(
        CreateOrderInteractor,
        user_repo=user_repo,
        order_repo=order_repo,
        promo_code_repo=promo_code_repo,
        product_repo=product_repo,
        notification_bus=notification_bus,
        payment_url_gateway=payment_url_gateway,
        delivery_price=Money(os.environ['DELIVERY_PRICE']),
    )
    payment_accept_service = providers.Factory(
        PaymentAcceptService,
        order_repo=order_repo,
    )
    call_me_interactor = providers.Factory(
        CallMeInteractor,
        notification_bus=notification_bus,
    )
    cart_service = providers.Factory(
        CartService,
    )


container = Container()
