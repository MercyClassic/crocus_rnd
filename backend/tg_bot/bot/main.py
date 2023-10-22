import handlers
from aiogram import executor
from create_bot import dp
from middlewares import AlbumMiddleware


def bot_run():
    dp.middleware.setup(AlbumMiddleware())
    handlers.admin.register_admin_handlers(dp)
    handlers.background_image.register_background_image_handlers(dp)
    handlers.cancel_state.register_cancel_handler(dp)
    handlers.category_create.register_category_create_handlers(dp)
    handlers.get_order_list.register_get_order_list_handlers(dp)
    handlers.product_create.register_product_create_handlers(dp)
    handlers.others.register_other_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    bot_run()