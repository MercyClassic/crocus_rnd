import asyncio
import copy
import logging
import os
from hashlib import sha256

import rollbar
from bot.handlers.notifications import send_notification_about_new_order

from payments.models import Order

logger = logging.getLogger('payment')


def check_payment_token(request_data: dict) -> bool:
    data = copy.copy(request_data)
    request_token = data.pop('Token')
    data.pop('Data')
    data.update({'Password': os.getenv('TINKOFF_PASSWORD')})
    data['Success'] = str(data['Success']).lower()
    token_data = tuple(map(lambda tup: str(tup[1]), sorted(data.items())))
    generated_token = sha256(''.join(token_data).encode('utf-8')).hexdigest()
    return request_token == generated_token


def payment_acceptance(request_data: dict) -> bool:
    if request_data.get('Status') == 'AUTHORIZED':
        return True
    try:
        order = Order.objects.only('id').get(uuid=request_data['OrderId'])
    except Order.DoesNotExist:
        message = (
            f'Ошибка при попытке найти заказ, uuid заказа: {request_data["OrderId"]},'
            f' id оплаты  в системе банка: {request_data["PaymentId"]}',
        )
        rollbar.report_message(message)
        logger.warning(message)
        return False
    if not check_payment_token(request_data):
        message = (
            f'Ошибка при сравнении токенов,'
            f' id заказа: {request_data["OrderId"]}, токен: {request_data["Token"]}',
        )
        rollbar.report_message(message)
        logger.warning(message)
        return False
    if request_data.get('Success') and request_data.get('Status') == 'CONFIRMED':
        order.is_paid = True
        order.save()
        logger.info(f'Заказ с id: {request_data["OrderId"]} - успешно оплачен')
        asyncio.run(send_notification_about_new_order(order.id))
    elif not request_data.get('Success'):
        order.delete()
        logger.warning(
            f'Заказ с id: {request_data["OrderId"]} - не был оплачен,'
            f'id в системе банка:{request_data["PaymentId"]},'
            f' код ошибки: {request_data["ErrorCode"]}',
        )
    return True
