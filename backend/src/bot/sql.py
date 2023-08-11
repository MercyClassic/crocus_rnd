import logging
import os

import psycopg2
from dotenv import load_dotenv

from bot import schemas

load_dotenv()


logger = logging.getLogger('telegram_errors')


def connection_to_db(func):
    def inner():
        try:
            connection = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database=os.getenv('POSTGRES_DB'),
            )
            ret = func(connection=connection)
            return ret
        except Exception as e:
            logger.error(e)
        finally:
            if connection:
                connection.close()
    return inner


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@connection_to_db
def get_paid_orders(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT o.id, o.amount, o.delivering, o.created_at, o.without_calling,
        o.delivery_date, o.delivery_time, o.delivery_address, o.note, o.cash,
        json_object_agg(p.title, op.count) as products
        FROM payments_order o INNER JOIN payments_orderproduct op ON o.id=op.order_id
        INNER JOIN products_product p ON op.product_id=p.id WHERE o.is_paid=false GROUP BY o.id;
        """)
        return [schemas.OrderData(**product) for product in dict_fetchall(cursor)]
