import os

from handlers.others import unknown_command

admin_ids = [int(admin_id) for admin_id in os.getenv('ADMIN_TG_BOT_IDS').split(', ')]
owner_ids = [int(owner_id) for owner_id in os.getenv('OWNER_TG_BOT_IDS').split(', ')]


def command_for(permission_level: str):
    def decorator(func):
        def wrapper(*args):
            message = args[0]
            if (permission_level == 'admin' and message.from_user.id in admin_ids) or (
                permission_level == 'owner' and message.from_user.id in owner_ids
            ):
                ret = func(*args)
                return ret
            return unknown_command(message)

        return wrapper

    return decorator


def slugify_string(string: str) -> str:
    return string.translate(
        str.maketrans(
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ’',
            'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA__',
        ),
    )


def validate_title(title: str) -> bool:
    return not any(i in '!@#$%^&*()+=`~;:"[]{}.,\'\\/' for i in title)
