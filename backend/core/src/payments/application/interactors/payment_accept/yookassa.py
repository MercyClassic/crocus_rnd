import logging

from payments.application.interactors.payment_accept.interface import (
    PaymentAcceptServiceInterface,
)
from payments.db.repositories.order import OrderRepository

logger = logging.getLogger(__name__)


class PaymentAcceptService(PaymentAcceptServiceInterface):
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def handle_webhook(self, request_data: dict) -> bool:
        order_uuid = request_data['object']['metadata']['order_id']
        logger.info(f'Подтверждение заказа. Входные данные: {request_data}')
        order = self._order_repo.get(order_uuid)
        if request_data['event'] == 'payment.succeeded':
            if (
                request_data['object']['status'] == 'succeeded'
                and request_data['object']['paid'] is True
            ):
                order.mark_as_paid()
                self._order_repo.update(order)
                logger.info(f'Заказ с id: {order_uuid} успешно оплачен')
                return True
            else:
                self._order_repo.delete(order_uuid)
                logger.info(f'Заказ с id: {order_uuid} не оплачен и был удалён')
                return True
        return False
