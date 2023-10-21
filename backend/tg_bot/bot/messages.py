# LONG BOT MESSAGES
from db.models import Order

admin_help_text = (
    'Доступные команды:'
    '\n/orderlist - Посмотреть оплаченные неготовые заказазы'
    '\n/adminpanel - Открыть административную панель'
    '\n/createproduct - Создать товар'
    '\n/createcategory - Создать категорию'
    '\n/setbgimage - Поменять главное изображение'
    '\n/downloadbgimage - Скачать главное изображение'
)


def get_order_detail_message(order: Order):
    products = ''
    for product_association in order.product_associations:
        products += (
            f'\t\t\t ‣ Название товара: {product_association.product.title},'
            f' Количетсво: {product_association.count}\n'
        )
    return (
        f'Информация о заказе:'
        f'\n • ID заказа: {order.id}'
        f'\n • Время создания заказа: {order.created_at}'
        f'\n • Сумма заказа: {order.amount}'
        f'\n • Ожидаемая дата получения: {order.delivery_date} '
        f'\n • Примечание: {order.note} '
        f'\n • С доставкой: {"Да" if order.delivering else "Нет"}'
        f'\n • Адрес доставки: {order.delivery_address} '
        f'\n • Время доставки: {order.delivery_time} '
        f'\n • Товары:\n{products}'
    )
