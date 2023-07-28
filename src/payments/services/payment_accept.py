import asyncio
import logging
import copy
import os
from hashlib import sha256

import rollbar

from bot.main import send_notification_about_new_order
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


def payment_acceptance(request: dict) -> bool:
    if request.get('Status') == 'AUTHORIZED':
        return True
    try:
        order = Order.objects.only('id').get(
            uuid=request['OrderId'],
        )
    except Order.DoesNotExist:
        message = (
            f'Ошибка при попытке найти заказ, uuid заказа: {request["OrderId"]},'
            f' id оплаты  в системе банка: {request["PaymentId"]}',
        )
        rollbar.report_message(message)
        logger.warning(message)
        return False
    if not check_payment_token(request):
        message = (
            f'Ошибка при сравнении токенов,'
            f' id заказа: {request["OrderId"]}, токен: {request["Token"]}',
        )
        rollbar.report_message(message)
        logger.warning(message)
        return False
    if request.get('Success') and request.get('Status') == 'CONFIRMED':
        order.is_paid = True
        order.save()
        logger.info(f'Заказ с id: {request["OrderId"]} - успешно оплачен')
        asyncio.run(send_notification_about_new_order(order.id))
    elif not request.get('Success'):
        order.delete()
        logger.warning(
            f'Заказ с id: {request["OrderId"]} - не был оплачен,'
            f'id в системе банка:{request["PaymentId"]}, код ошибки: {request["ErrorCode"]}',
        )
    return True
