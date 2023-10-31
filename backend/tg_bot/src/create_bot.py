import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('telegram_errors')

bot = Bot(os.getenv('BOT_TOKEN'))

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.errors_handler()
async def errors_handler(update, exception):
    logger.error(
        exception,
        extra={
            'user_id': update.message.from_user.id,
            'message_id': update.message.message_id,
        },
    )
    return True
