import asyncio

from rest_framework.request import Request

from bot.main import send_notification_about_new_call_me
from utils.pause import check_for_pause_timer, set_pause_timer


def create_call_me_request(request: Request, phone_number: str) -> bool | None:
    if not check_for_pause_timer(request, 'call_me'):
        return False
    set_pause_timer(request, 'call_me')

    asyncio.run(
        send_notification_about_new_call_me(phone_number),
    )
