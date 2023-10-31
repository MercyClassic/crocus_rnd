from dependency_injector.wiring import Provide, inject

from container import Container
from rabbitmq.notifications import NotificationBus


@inject
def start_consuming(
    notification_bus: NotificationBus = Provide[Container.notification_bus],
):
    notification_bus.receive_notification()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__, 'handlers.notifications'])
    start_consuming()
