from rest_framework.request import Request

from rabbitmq.notifications import NotificationBus
from utils.pause import check_for_pause_timer


class CallMeService:
    def __init__(self, notification_bus: NotificationBus):
        self.notification_bus = notification_bus

    def create_call_me_request(
        self,
        request: Request,
        phone_number: str,
    ) -> bool:
        if not check_for_pause_timer(request, 'call_me'):
            return False

        with self.notification_bus:
            self.notification_bus.send_call_me_request_notification(phone_number)

        return True
