import logging
from logging import config as logging_config

from aiogram import Router, types

from config import Config, get_logging_dict

router = Router()


@router.errors()
async def handle_unexpected_errors(
    event: types.ErrorEvent,
    config: Config,
):
    logging_dict = get_logging_dict(config.root_dir)
    logging_config.dictConfig(logging_dict)
    logger = logging.getLogger('main')

    logger.error(
        event.exception,
        exc_info=True,
    )
    await event.update.message.answer(
        'Возникли неожиданные проблемы, обратитесь к администратуору!',
    )
