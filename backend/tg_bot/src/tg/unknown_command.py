from aiogram import Bot, Router, types

router = Router()


@router.message()
async def unknown_command(
    message: types.Message,
    bot: Bot,
):
    await bot.send_message(
        message.from_user.id,
        'Неизвестная команда. Проверьте сообщение на опечатку',
    )
