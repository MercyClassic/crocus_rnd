import copy
import logging
import os
from hashlib import sha256

import rollbar

from payments.infrastructure.repositores.order import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentAcceptService:
    def __init__(
        self,
        payment_repo: PaymentRepository,
        request_data: dict,
    ):
        self.payment_repo = payment_repo
        self._request_data = request_data

    def check_payment_token(self) -> bool:
        data = copy.copy(self._request_data)
        request_token = data.pop('Token')
        data.pop('Data')
        data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
        data['Success'] = str(data['Success']).lower()
        token_data = tuple(map(lambda tup: str(tup[1]), sorted(data.items())))
        generated_token = sha256(''.join(token_data).encode('utf-8')).hexdigest()
        return request_token == generated_token

    def handle_webhook(self) -> bool:
        if self._request_data.get('Status') == 'AUTHORIZED':
            return True
        order_uuid = self._request_data['OrderId']
        order = self.payment_repo.get_order_by_uuid(order_uuid)
        if not order:
            message = (
                f'Ошибка при попытке найти заказ, uuid заказа: {order_uuid},'
                f' id оплаты  в системе банка: {self._request_data["PaymentId"]}',
            )
            rollbar.report_message(message)
            logger.warning(message)
            return False
        if not self.check_payment_token():
            message = (
                f'Ошибка при сравнении токенов,'
                f' id заказа: {order_uuid}, токен: {self._request_data["Token"]}',
            )
            rollbar.report_message(message)
            logger.warning(message)
            return False
        if self._request_data.get('Success') and self._request_data.get('Status') == 'CONFIRMED':
            self.payment_repo.set_is_paid_to_order(order)
            logger.info(f'Заказ с id: {order_uuid} - успешно оплачен')
        elif not self._request_data.get('Success'):
            self.payment_repo.delete_order(order_uuid)
            logger.warning(
                f'Заказ с id: {order_uuid} - не был оплачен,'
                f'id в системе банка:{self._request_data["PaymentId"]},'
                f' код ошибки: {self._request_data["ErrorCode"]}',
            )
        return True
