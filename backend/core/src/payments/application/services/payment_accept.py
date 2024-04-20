import copy
import logging
import os
from hashlib import sha256

import rollbar

from payments.infrastructure.db.repositories.order import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentAcceptService:
    def __init__(
        self,
        payment_repo: PaymentRepository,
    ):
        self._payment_repo = payment_repo

    def check_payment_token(self, request_data: dict) -> bool:
        data = copy.copy(request_data)
        request_token = data.pop('Token')
        data.pop('Data')
        data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
        data['Success'] = str(data['Success']).lower()
        token_data = tuple(map(lambda tup: str(tup[1]), sorted(data.items())))
        generated_token = sha256(''.join(token_data).encode('utf-8')).hexdigest()
        return request_token == generated_token

    def handle_webhook(self, request_data: dict,) -> bool:
        if request_data.get('Status') == 'AUTHORIZED':
            return True
        order_uuid = request_data['OrderId']
        order = self._payment_repo.get_order_by_uuid(order_uuid)
        if not order:
            message = (
                f'Ошибка при попытке найти заказ, uuid заказа: {order_uuid}, '
                f"id оплаты  в системе банка: {request_data['PaymentId']}",
            )
            rollbar.report_message(message)
            logger.warning(message)
            return False
        if not self.check_payment_token(request_data):
            message = (
                f'Ошибка при сравнении токенов, '
                f'id заказа: {order_uuid}, токен: {request_data["Token"]}',
            )
            rollbar.report_message(message)
            logger.warning(message)
            return False
        if request_data.get('Success') and request_data.get('Status') == 'CONFIRMED':
            self._payment_repo.set_is_paid_to_order(order)
            logger.info(f'Заказ с id: {order_uuid} - успешно оплачен')
        elif not request_data.get('Success'):
            self._payment_repo.delete_order(order_uuid)
            logger.warning(
                f'Заказ с id: {order_uuid} - не был оплачен,'
                f"id в системе банка:{request_data['PaymentId']}, "
                f"код ошибки: {request_data['ErrorCode']}",
            )
        return True
