from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

router = Router()


@router.message(State('*'), Command('cancel'))
async def cancel_handler(
    message: types.Message,
    state: FSMContext,
):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()

    await message.reply('Создание отменено')
