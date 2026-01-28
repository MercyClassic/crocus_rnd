import os
from collections.abc import AsyncGenerator

from aiogram import Bot

from main.config import Config, load_config
from db.repositories import CoreRepository
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from notification_bus.sender import NotificationSender


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_async_session_maker(self) -> async_sessionmaker:
        engine = create_async_engine(
            os.environ['DB_URI'],
            isolation_level='REPEATABLE READ',
        )
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide()
    async def get_async_session(
        self,
        async_session_maker: async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        return load_config()

    @provide()
    async def get_core_repository(self, session: AsyncSession) -> CoreRepository:
        return CoreRepository(session=session)

    @provide(scope=Scope.APP)
    async def get_notification_sender(self, app_config: Config) -> NotificationSender:
        return NotificationSender(
            bot=Bot(app_config.bot_token),
            domain=app_config.domain,
            admin_panel_order_url=app_config.admin_panel_order_url,
            notification_receivers=app_config.to_notificate_telegram_ids,
        )
