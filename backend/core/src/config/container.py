import os

from accounts.repositories import UserRepository
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from notification_bus.services.sender import NotificationBus
from payments.application.services.call_me import CallMeService
from payments.application.services.payment_accept import PaymentAcceptService
from payments.application.services.payment_create import PaymentCreateService
from payments.infrastructure.db.repositories.order import PaymentRepository
from payments.infrastructure.db.repositories.tinkoff import TinkoffPaymentUrlGateway
from products.services.cart import CartService


class Container(DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)
    payment_repo = providers.Factory(PaymentRepository)
    notification_bus = providers.Factory(
        NotificationBus,
        host=os.environ['RABBITMQ_HOST'],
        port=os.environ['RABBITMQ_PORT'],
    )
    payment_url_gateway = providers.Factory(
        TinkoffPaymentUrlGateway,
        terminal_key=os.environ['TINKOFF_TERMINAL_KEY'],
        taxation=os.environ['TINKOFF_TAXATION'],
        password=os.environ['TINKOFF_PASSWORD'],
        tax=os.environ['TINKOFF_TAX'],
        delivery_price=int(os.environ['DELIVERY_PRICE']),
        payment_url=os.environ['TINKOFF_PAYMENT_URL'],
    )

    payment_create_service = providers.Factory(
        PaymentCreateService,
        user_repo=user_repo,
        payment_repo=payment_repo,
        notification_bus=notification_bus,
        payment_url_gateway=payment_url_gateway,
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
