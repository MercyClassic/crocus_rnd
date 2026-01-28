import logging
import uuid
from decimal import Decimal

from accounts.repositories import UserRepository
from notification_bus.interfaces.sender import NotificationBusInterface


from payments.application.dto.order import OrderDTO
from payments.application.gateways.interface import PaymentUrlGatewayInterface
from payments.db.repositories.order import (
    OrderRepository,
    PromoCodeRepository,
)
from payments.db.repositories.product import ProductRepository
from payments.entities.order import Order, OrderProduct, PromoCode
from payments.entities.order_id import OrderId
from payments.entities.value_objects import Money

logger = logging.getLogger(__name__)


class CreateOrderInteractor:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        promo_code_repo: PromoCodeRepository,
        user_repo: UserRepository,
        notification_bus: NotificationBusInterface,
        payment_url_gateway: PaymentUrlGatewayInterface,
        delivery_price: Money,
    ):
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._promo_code_repo = promo_code_repo
        self._user_repo = user_repo
        self._notification_bus = notification_bus
        self._payment_url_gateway = payment_url_gateway
        self._delivery_price = delivery_price

    def _get_order(self, order_data: OrderDTO) -> Order:
        order_products = self._get_order_products(order_data.products)
        promo_code = self._get_promo_code(order_data.promo_code)
        user_account = self._user_repo.get_or_create_customer(
            order_data.customer_phone_number,
            order_data.customer_name,
        )
        order = Order(
            id=OrderId(uuid.uuid4()),
            user_id=user_account.id,
            amount=order_data.amount,
            delivering=order_data.delivering,
            without_calling=order_data.without_calling,
            customer_email=order_data.customer_email,
            customer_phone_number=order_data.customer_phone_number,
            receiver_name=order_data.receiver_name,
            receiver_phone_number=order_data.receiver_phone_number,
            delivery_address=order_data.delivery_address,
            delivery_date=order_data.delivery_date,
            delivery_time=order_data.delivery_time,
            note=order_data.note,
            cash=order_data.cash,
            products=order_products,
            promo_code=promo_code,
            delivery_price=self._delivery_price,
            is_paid=False,
        )
        return order

    def _get_payment_url(self, order: Order) -> str:
        try:
            result = self._payment_url_gateway.get_payment_url(
                order_uuid=str(order.id),
                amount=order.amount,
                products=order.products,
                with_delivery=order.delivering,
                customer_phone_number=order.customer_phone_number,
                customer_email=order.customer_email,
                discount_coefficient=(
                    order.promo_code.get_discount_coefficient(order.amount)
                    if order.promo_code
                    else Decimal(1)
                ),
            )
        except Exception as exc:
            logger.error(f'Ошибка при получении ссылки на оплату: {exc}')
            raise exc

    def _order_created(self, order: Order) -> None:
        try:
            self._notification_bus.order_created(order.order_id)
        except Exception as exc:
            logger.error(f'Ошибка при отправке уведомления: {exc}')

    def __call__(self, order_data: OrderDTO) -> str:
        order = self._get_order(order_data)
        if order.cash:
            result = 'OK'
        else:
            result = self._get_payment_url(order)
        self._order_repo.save(order)
        self._order_created(order)
        return result

    def _get_order_products(self, products: dict) -> list[OrderProduct]:
        return [
            OrderProduct(
                product_id=product_data.id,
                slug=product_data.slug,
                count=int(products.get(product_data.slug, 0)),
                title=product_data.title,
                price=Money(product_data.price),
            )
            for product_data in self._product_repo.list(list(products.keys()))
        ]

    def _get_promo_code(self, code: str | None) -> PromoCode | None:
        if not code:
            return None

        promo_code_data = self._promo_code_repo.get(code)
        if not promo_code_data:
            return None

        return PromoCode(
            code=promo_code_data.code,
            discount_percent=promo_code_data.discount_percent,
            is_active=promo_code_data.is_active,
        )
