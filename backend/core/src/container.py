from dependency_injector import containers, providers

from accounts.repositories import UserRepository
from payments.repositories import PaymentRepository
from payments.services.call_me import CallMeService
from payments.services.payment_create import PaymentCreateService
from rabbitmq.notifications import NotificationBus


class Container(containers.DeclarativeContainer):
    payment_repo = providers.Factory(
        PaymentRepository,
    )

    user_repo = providers.Factory(
        UserRepository,
    )

    notification_bus = providers.Factory(
        NotificationBus,
    )

    payment_service = providers.Factory(
        PaymentCreateService,
        payment_repo,
        user_repo,
        notification_bus,
    )

    call_me_service = providers.Factory(
        CallMeService,
        notification_bus,
    )


container = Container()
