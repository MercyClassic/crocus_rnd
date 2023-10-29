from db.database import get_async_session
from dependency_injector import containers, providers
from repositories.core import CoreRepository


class Container(containers.DeclarativeContainer):
    session = providers.Resource(
        get_async_session,
    )

    core_repo = providers.Factory(
        CoreRepository,
        session,
    )
