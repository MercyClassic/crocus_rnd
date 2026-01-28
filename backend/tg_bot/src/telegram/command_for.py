import functools

from telegram.unknown_command import unknown_command
from main.config import load_config


def command_for(permission_level: str):
    app_config = load_config()

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            message = args[0]
            if (
                permission_level == 'admin'
                and message.from_user.id in app_config.tg_admin_ids
            ) or (
                permission_level == 'owner'
                and message.from_user.id in app_config.tg_owner_ids
            ):
                return await func(*args, **kwargs)
            return unknown_command(message, kwargs['bot'])

        return wrapper

    return decorator
