import logging

from aiogram import Router, types

router = Router()


@router.errors()
async def handle_unexpected_errors(
    event: types.ErrorEvent,
):
    logger = logging.getLogger("main")
    logger.error(
        event.exception,
        exc_info=True,
    )
    if event.update.message:
        await event.update.message.answer(
            "Возникли неожиданные проблемы, обратитесь к администратору!",
        )
