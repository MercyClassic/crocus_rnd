import functools
import json
import os

from tg.unknown_command import unknown_command

admin_ids = [int(telegram_id) for telegram_id in json.loads(os.environ['ADMIN_TG_BOT_IDS'])]
owner_ids = [int(telegram_id) for telegram_id in json.loads(os.environ['OWNER_TG_BOT_IDS'])]



def command_for(permission_level: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = args[0]
            if (permission_level == 'admin' and message.from_user.id in admin_ids) or (
                permission_level == 'owner' and message.from_user.id in owner_ids
            ):
                return func(*args, **kwargs)
            return unknown_command(message, kwargs['bot'])
        return wrapper
    return decorator
