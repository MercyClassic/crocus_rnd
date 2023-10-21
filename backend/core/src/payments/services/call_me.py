import asyncio

from bot.handlers.notifications import send_notification_about_new_call_me
from bot.utils import check_for_pause_timer, set_pause_timer
from rest_framework.request import Request


def create_call_me_request(request: Request, phone_number: str) -> bool | None:
    if not check_for_pause_timer(request, 'call_me'):
        return False
    set_pause_timer(request, 'call_me')

    asyncio.run(
        send_notification_about_new_call_me(phone_number),
    )
    return True
