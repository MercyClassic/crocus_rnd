import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from provider import CoreProvider
from tg.middlewares import AlbumMiddleware
from tg.routers import (
    admin_router,
    bg_image_router,
    cancel_state_router,
    category_create_router,
    errors_router,
    order_router,
    product_create_router,
    unknown_command_router,
)

logger = logging.getLogger('main')


async def main() -> None:
    tg_config = load_config()
    bot = Bot(tg_config.bot_token)
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
    setup_dishka(container=container, router=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f'Bot started {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
