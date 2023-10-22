import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('telegram_errors')


bot = Bot(os.getenv('BOT_TOKEN'))

domain = os.getenv('DOMAIN')
admin_panel_product_url = os.getenv('ADMIN_PANEL_PRODUCT_URL')
admin_panel_order_url = os.getenv('ADMIN_PANEL_ORDER_URL')
admin_panel_category_url = os.getenv('ADMIN_PANEL_CATEGORY_URL')
admin_panel_url = os.getenv('ADMIN_PANEL_URL')

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
