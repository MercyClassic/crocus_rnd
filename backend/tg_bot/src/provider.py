import os
from collections.abc import AsyncGenerator

from config import Config, load_config
from db.repositories import CoreRepository
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_async_session_maker(self) -> async_sessionmaker:
        engine = create_async_engine(
            os.environ['db_uri'],
            isolation_level='REPEATABLE READ',
            connect_args={'options': '-c timezone=Europe/Moscow'},
        )
        return async_sessionmaker(
            engine=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        return load_config()

    @provide()
    async def get_async_session(
            self,
            async_session_maker: async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker as session:
            yield session

    @provide()
    async def get_core_repository(self, session: AsyncSession) -> CoreRepository:
        return CoreRepository(session=session)
