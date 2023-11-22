import logging
import os
from logging import config

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import get_config, get_logging_dict

load_dotenv()

config.dictConfig(get_logging_dict(get_config()))
logger = logging.getLogger(__name__)

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
