from aiogram import Dispatcher


async def cancel_handler(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.reply('Создание отменено')


def register_cancel_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
