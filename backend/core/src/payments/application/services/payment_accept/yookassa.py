import logging

from payments.application.interfaces.services.payment_accept import (
    PaymentAcceptServiceInterface,
)
from payments.infrastructure.db.repositories.order import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentAcceptService(PaymentAcceptServiceInterface):
    def __init__(
        self,
        payment_repo: PaymentRepository,
    ):
        self._payment_repo = payment_repo

    def handle_webhook(self, request_data: dict) -> bool:
        order_uuid = request_data['object']['metadata']['order_id']
        logger.info(f'Подтверждение заказа. Входные данные: {request_data}')
        order = self._payment_repo.get_order_by_uuid(order_uuid)
        if request_data['event'] == 'payment.succeeded':
            if (
                request_data['object']['status'] == 'succeeded'
                and request_data['object']['paid'] is True
            ):
                self._payment_repo.set_is_paid_to_order(order)
                logger.info(f'Заказ с id: {order_uuid} успешно оплачен')
                return True
            else:
                self._payment_repo.delete_order(order_uuid)
                logger.info(f'Заказ с id: {order_uuid} не оплачен и был удалён')
                return True
        return False
