import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from db.database import create_async_session_maker
from logic import handlers
from logic.middlewares import AlbumMiddleware, DependencyMiddleware

from config import load_config


async def main() -> None:
    tg_config = load_config()
    bot = Bot(tg_config.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    async_session_maker = create_async_session_maker(os.environ['db_uri'])
    dp.update.outer_middleware(AlbumMiddleware())
    dp.update.outer_middleware(
        DependencyMiddleware(
            bot,
            tg_config,
            async_session_maker,
        ),
    )

    dp.include_router(handlers.admin_router)
    dp.include_router(handlers.bg_image_router)
    dp.include_router(handlers.cancel_state_router)
    dp.include_router(handlers.category_create_router)
    dp.include_router(handlers.get_order_list_router)
    dp.include_router(handlers.product_create_router)
    dp.include_router(handlers.others_router)
    dp.include_router(handlers.errors_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
