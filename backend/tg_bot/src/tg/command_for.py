import functools
import os

from tg.unknown_command import unknown_command

admin_ids = [int(admin_id) for admin_id in os.environ['ADMIN_TG_BOT_IDS'].split(', ')]
owner_ids = [int(owner_id) for owner_id in os.environ['OWNER_TG_BOT_IDS'].split(', ')]


def command_for(permission_level: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            message = args[0]
            if (permission_level == 'admin' and message.from_user.id in admin_ids) or (
                permission_level == 'owner' and message.from_user.id in owner_ids
            ):
                return func(*args)
            return unknown_command(message)
        return wrapper
    return decorator
