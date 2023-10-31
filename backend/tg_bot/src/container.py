from db.database import get_async_session
from dependency_injector import containers, providers
from repositories.core import CoreRepository

from config import get_config
from rabbitmq.notifications import NotificationBus


class Container(containers.DeclarativeContainer):
    session = providers.Resource(
        get_async_session,
    )

    core_repo = providers.Factory(
        CoreRepository,
        session,
    )

    config = providers.Factory(
        get_config,
    )

    notification_bus = providers.Factory(
        NotificationBus,
    )
