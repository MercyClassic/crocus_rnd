from typing import Callable, Dict

from aiogram import BaseMiddleware, Bot, types
from db.database import get_async_session
from db.repositories import CoreRepository
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import Config


class DependencyMiddleware(BaseMiddleware):
    def __init__(
        self,
        bot: Bot,
        config: Config,
        async_session_maker: async_sessionmaker,
    ):
        self.bot = bot
        self.config = config
        self.async_session_maker = async_session_maker

    async def create_core_repo(self) -> CoreRepository:
        session = await anext(get_async_session(self.async_session_maker))
        return CoreRepository(session)

    async def __call__(
        self,
        handler: Callable,
        event: types.TelegramObject,
        data: Dict,
    ):
        data['core_repo'] = await self.create_core_repo()
        data['config'] = self.config
        await handler(event, data)
