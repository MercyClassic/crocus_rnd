from accounts.repositories import UserRepository
from config.settings import RABBITMQ_HOST
from interfaces.notification_bus import NotificationBusInterface
from interfaces.services.call_me import CallMeServiceInterface
from interfaces.services.payment_accept import PaymentAcceptServiceInterface
from interfaces.services.payment_create import PaymentCreateServiceInterface
from ioc.container import DependencyContainer
from payments.repositories import PaymentRepository


class DependencyProvider:
    def __init__(self, container: DependencyContainer):
        self.__container = container

    def provide_notification_bus(self):
        return self.__container.get(NotificationBusInterface)(
            host=RABBITMQ_HOST,
            port=5672,
        )

    def provide_payment_create_service(self) -> PaymentCreateServiceInterface:
        notification_bus = self.provide_notification_bus()
        return self.__container.get(PaymentCreateServiceInterface)(
            payment_repo=PaymentRepository(),
            user_repo=UserRepository(),
            notification_bus=notification_bus,
        )

    def provide_call_me_service(self) -> CallMeServiceInterface:
        notification_bus = self.provide_notification_bus()
        return self.__container.get(CallMeServiceInterface)(
            notification_bus=notification_bus,
        )

    def provide_payment_accept_service(self, request_data: dict) -> PaymentAcceptServiceInterface:
        return self.__container.get(PaymentAcceptServiceInterface)(
            payment_repo=PaymentRepository(),
            request_data=request_data,
        )
