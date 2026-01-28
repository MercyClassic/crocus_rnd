import copy
from datetime import datetime

from payments.domain.entities.base import Entity
from payments.domain.entities.order_id import OrderId
from payments.domain.entities.value_objects import Money
from payments.domain.exceptions.validation import ValidationError


class OrderProduct(Entity):
    def __init__(
        self,
        id: int,
        slug: str,
        count: int,
        title: str,
        price: Money,
    ):
        self._id = id
        self._slug = slug
        self._count = count
        self._title = title
        self._price = price

        if self._count < 1:
            raise ValidationError('Product count must be at least 1')

    @property
    def id(self) -> int:
        return self._id

    @property
    def slug(self) -> str:
        return self._slug

    @property
    def title(self) -> str:
        return self._title

    @property
    def count(self) -> int:
        return self._count

    @property
    def price(self) -> Money:
        return self._price

    @property
    def total_price(self) -> Money:
        return self._price * self._count


class PromoCode(Entity):
    def __init__(
        self,
        id: int,
        code: str,
        value: Money,
        is_percent: bool,
        is_active: bool,
    ):
        self._id = id
        self._code = code
        self._value = value
        self._is_percent = is_percent
        self._is_active = is_active

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    def get_discount_coefficient(self, amount: Money) -> Money:
        if not self._is_active:
            return Money(1)

        if self._is_percent:
            return Money(1 - self._value / 100)
        else:
            return Money(1 - self._value / amount)


class Order(Entity):
    def __init__(
        self,
        id: OrderId,
        user_id: int,
        amount: Money,
        is_paid: bool,
        delivering: bool,
        without_calling: bool,
        customer_email: str | None,
        receiver_name: str,
        receiver_phone_number: str,
        delivery_address: str | None,
        delivery_date: datetime,
        delivery_time: str | None,
        note: str,
        cash: bool,
        delivery_price: Money,
        products: list[OrderProduct],
        products_count: dict[str, int],
        customer_phone_number: str | None = None,
        promo_code: PromoCode | None = None,
    ):
        self._id = id
        self._user_id = user_id
        self._is_paid = is_paid
        self._delivering = delivering
        self._without_calling = without_calling
        self._customer_email = customer_email
        self._customer_phone_number = customer_phone_number
        self._receiver_name = receiver_name
        self._receiver_phone_number = receiver_phone_number
        self._delivery_address = delivery_address
        self._delivery_date = delivery_date
        self._delivery_time = delivery_time
        self._note = note
        self._cash = cash
        self._products = products
        self._products_count = products_count
        self._promo_code = promo_code
        self._delivery_price = delivery_price

        self._amount = sum(product.total_price for product in self._products)
        self._amount *= self.discount_coefficient

        if self._delivering:
            self._amount += self._delivery_price

        if self._amount != amount:
            raise ValidationError('Requested amount not equals calculated amount')

        if self._delivery_date.date() < datetime.utcnow().date():
            raise ValidationError('Delivery date cannot be in the past')

        max_amount = Money(50000) + (
            self._delivery_price if self._delivering else Money(0)
        )
        if self._amount > max_amount:
            raise ValidationError('Order amount exceeds maximum limit')

        if not self._products:
            raise ValidationError('Order must contain at least one product')

    @property
    def discount_coefficient(self) -> Money:
        if self._promo_code:
            return self._promo_code.get_discount_coefficient(self._amount)
        return Money(1)

    def mark_as_paid(self):
        self._is_paid = True

    @property
    def id(self) -> OrderId:
        return self._id

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def is_paid(self) -> bool:
        return self._is_paid

    @property
    def products(self) -> list[OrderProduct]:
        return copy.deepcopy(self._products)

    @property
    def products_count(self) -> dict[str, int]:
        return copy.deepcopy(self._products_count)

    @property
    def promo_code(self) -> PromoCode:
        return copy.deepcopy(self._promo_code)

    @property
    def delivering(self) -> bool:
        return self._delivering

    @property
    def customer_phone_number(self) -> str:
        return self._customer_phone_number

    @property
    def customer_email(self) -> str:
        return self._customer_email

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def cash(self) -> bool:
        return self._cash

    @property
    def note(self) -> str:
        return self._note

    @property
    def delivery_time(self) -> str:
        return self._delivery_time

    @property
    def delivery_date(self) -> datetime:
        return self._delivery_date

    @property
    def receiver_phone_number(self) -> str:
        return self._receiver_phone_number

    @property
    def delivery_address(self) -> str:
        return self._delivery_address

    @property
    def receiver_name(self) -> str:
        return self._receiver_name

    @property
    def without_calling(self) -> bool:
        return self._without_calling
