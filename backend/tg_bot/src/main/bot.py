import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from main.config import Config
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from main.provider import CoreProvider
from telegram.middlewares import AlbumMiddleware
from telegram.routers import (
    admin_router,
    bg_image_router,
    cancel_state_router,
    category_create_router,
    errors_router,
    order_router,
    product_create_router,
    unknown_command_router,
)

logger = logging.getLogger("main")


async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(AlbumMiddleware())

    dp.include_router(admin_router)
    dp.include_router(bg_image_router)
    dp.include_router(cancel_state_router)
    dp.include_router(category_create_router)
    dp.include_router(order_router)
    dp.include_router(product_create_router)
    dp.include_router(unknown_command_router)
    dp.include_router(errors_router)

    container = make_async_container(CoreProvider())
    setup_dishka(container=container, router=dp, auto_inject=True)

    app_config = await container.get(Config)
    bot = Bot(app_config.bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f'Bot started {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
