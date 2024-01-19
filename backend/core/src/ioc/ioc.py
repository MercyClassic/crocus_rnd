from interfaces.notification_bus import NotificationBusInterface
from interfaces.services.call_me import CallMeServiceInterface
from interfaces.services.payment_accept import PaymentAcceptServiceInterface
from interfaces.services.payment_create import PaymentCreateServiceInterface
from ioc.container import DependencyContainer
from ioc.provider import DependencyProvider
from payments.services.call_me import CallMeService
from payments.services.payment_accept import PaymentAcceptService
from payments.services.payment_create import PaymentCreateService
from rabbitmq.notification_bus import NotificationBus

container = DependencyContainer()
container.bind_multiple(
    {
        PaymentCreateServiceInterface: PaymentCreateService,
        PaymentAcceptServiceInterface: PaymentAcceptService,
        CallMeServiceInterface: CallMeService,
        NotificationBusInterface: NotificationBus,
    },
)
provider = DependencyProvider(container)
