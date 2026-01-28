import copy
import logging
import os
from hashlib import sha256

from payments.application.interactors.payment_accept.interface import (
    PaymentAcceptServiceInterface,
)
from payments.db.repositories.order import OrderRepository

logger = logging.getLogger(__name__)


class PaymentAcceptService(PaymentAcceptServiceInterface):
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def check_payment_token(self, request_data: dict) -> bool:
        data = copy.copy(request_data)
        request_token = data.pop('Token')
        data.pop('Data')
        data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
        data['Success'] = str(data['Success']).lower()
        token_data = tuple(item for _, item in sorted(data.items()))
        generated_token = sha256(''.join(token_data).encode('utf-8')).hexdigest()
        return request_token == generated_token

    def handle_webhook(self, request_data: dict) -> bool:
        if request_data.get('Status') == 'AUTHORIZED':
            return True
        order_uuid = request_data['OrderId']
        order = self._order_repo.get(order_uuid)
        if not order:
            message = (
                f'Ошибка при попытке найти заказ, uuid заказа: {order_uuid}, '
                f"id оплаты  в системе банка: {request_data['PaymentId']}",
            )
            logger.warning(message)
            return False
        if not self.check_payment_token(request_data):
            message = (
                f'Ошибка при сравнении токенов, '
                f'id заказа: {order_uuid}, токен: {request_data["Token"]}',
            )
            logger.warning(message)
            return False
        if request_data.get('Success') and request_data.get('Status') == 'CONFIRMED':
            order.mark_as_paid()
            self._order_repo.update(order)
            logger.info(f'Заказ с id: {order_uuid} - успешно оплачен')
        elif not request_data.get('Success'):
            self._order_repo.delete(order_uuid)
            logger.warning(
                f'Заказ с id: {order_uuid} - не был оплачен,'
                f"id в системе банка:{request_data['PaymentId']}, "
                f"код ошибки: {request_data['ErrorCode']}",
            )
        return True
