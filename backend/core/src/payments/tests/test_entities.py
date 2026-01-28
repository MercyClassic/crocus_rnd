import uuid
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

import pytest

from payments.domain.entities.order import Order, OrderProduct, PromoCode
from payments.domain.entities.order_id import OrderId
from payments.domain.entities.value_objects import Money
from payments.domain.exceptions.validation import ValidationError


@pytest.mark.parametrize(
    'count, should_raise',
    [
        (1, False),
        (5, False),
        (0, True),
        (-1, True),
    ],
)
def test_order_product_count_validation(count, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            OrderProduct(
                id=123,
                slug='s1',
                count=count,
                title='Product',
                price=Money(100),
            )
    else:
        product = OrderProduct(
            id=123,
            slug='s1',
            count=count,
            title='Product',
            price=Money(100),
        )
        assert product.count == count


@pytest.mark.parametrize(
    'price, count, expected_total',
    [
        (100, 1, 100),
        (100, 3, 300),
        (250, 2, 500),
    ],
)
def test_order_product_total_price(price, count, expected_total):
    product = OrderProduct(
        id=123,
        slug='s1',
        count=count,
        title='Product',
        price=Money(price),
    )

    assert product.total_price == Money(expected_total)


@pytest.mark.parametrize(
    'is_active, is_percent, value, amount, expected',
    [
        (False, True, 10, 1000, 1),
        (True, True, 10, 1000, 0.9),
        (True, False, 100, 1000, 0.9),
    ],
)
def test_promo_code_discount_coefficient(
    is_active,
    is_percent,
    value,
    amount,
    expected,
):
    promo = PromoCode(
        id=1,
        code='PROMO',
        value=Money(value),
        is_percent=is_percent,
        is_active=is_active,
    )

    coefficient = promo.get_discount_coefficient(Money(amount))
    assert coefficient == Money(expected).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP,
    )


def make_product(price=100, count=1):
    return OrderProduct(
        id=123,
        slug='s1',
        count=count,
        title='Product',
        price=Money(price),
    )


@pytest.mark.parametrize(
    'delivering, delivery_price',
    [
        (False, Money(0)),
        (True, Money(300)),
    ],
)
def test_order_success_creation(delivering, delivery_price):
    products = [make_product(100, 2)]
    base_amount = Money(200)
    expected_amount = base_amount + (delivery_price if delivering else Money(0))

    order = Order(
        id=OrderId(uuid.uuid4()),
        user_id=1,
        amount=expected_amount,
        is_paid=False,
        delivering=delivering,
        without_calling=False,
        customer_email='test@test.com',
        receiver_name='John',
        receiver_phone_number='+79999999999',
        delivery_address='Street' if delivering else None,
        delivery_date=datetime.utcnow() + timedelta(days=1),
        delivery_time=None,
        note='',
        cash=False,
        delivery_price=delivery_price,
        products=products,
        products_count={'p1': 2},
    )

    assert order.amount == expected_amount
    assert order.delivering is delivering


@pytest.mark.parametrize(
    'delivering, delivery_price',
    [
        (False, Money(0)),
        (True, Money(300)),
    ],
)
def test_order_success_creation(delivering, delivery_price):
    products = [make_product(100, 2)]
    base_amount = Money(200)
    expected_amount = base_amount + (delivery_price if delivering else Money(0))

    order = Order(
        id=OrderId(uuid.uuid4()),
        user_id=1,
        amount=expected_amount,
        is_paid=False,
        delivering=delivering,
        without_calling=False,
        customer_email='test@test.com',
        receiver_name='John',
        receiver_phone_number='+79999999999',
        delivery_address='Street' if delivering else None,
        delivery_date=datetime.utcnow() + timedelta(days=1),
        delivery_time=None,
        note='',
        cash=False,
        delivery_price=delivery_price,
        products=products,
        products_count={'p1': 2},
    )

    assert order.amount == expected_amount
    assert order.delivering is delivering


def test_order_with_percent_promo_code():
    promo = PromoCode(
        id=1,
        code='SALE10',
        value=Money(10),
        is_percent=True,
        is_active=True,
    )

    products = [make_product(100, 2)]  # 200
    discounted = Money(180)

    order = Order(
        id=OrderId(uuid.uuid4()),
        user_id=1,
        amount=discounted,
        is_paid=False,
        delivering=False,
        without_calling=False,
        customer_email=None,
        receiver_name='John',
        receiver_phone_number='+79999999999',
        delivery_address=None,
        delivery_date=datetime.utcnow() + timedelta(days=1),
        delivery_time=None,
        note='',
        cash=False,
        delivery_price=Money(0),
        products=products,
        products_count={'p1': 2},
        promo_code=promo,
    )

    assert order.amount == discounted


@pytest.mark.parametrize(
    'amount',
    [
        Money(100),
        Money(999),
    ],
)
def test_order_invalid_amount(amount):
    products = [make_product(100, 2)]

    with pytest.raises(ValidationError):
        Order(
            id=OrderId(uuid.uuid4()),
            user_id=1,
            amount=amount,
            is_paid=False,
            delivering=False,
            without_calling=False,
            customer_email=None,
            receiver_name='John',
            receiver_phone_number='+79999999999',
            delivery_address=None,
            delivery_date=datetime.utcnow() + timedelta(days=1),
            delivery_time=None,
            note='',
            cash=False,
            delivery_price=Money(0),
            products=products,
            products_count={'p1': 2},
        )


def test_order_delivery_date_in_past():
    products = [make_product()]

    with pytest.raises(ValidationError):
        Order(
            id=OrderId(uuid.uuid4()),
            user_id=1,
            amount=Money(100),
            is_paid=False,
            delivering=False,
            without_calling=False,
            customer_email=None,
            receiver_name='John',
            receiver_phone_number='+79999999999',
            delivery_address=None,
            delivery_date=datetime.utcnow() - timedelta(days=1),
            delivery_time=None,
            note='',
            cash=False,
            delivery_price=Money(0),
            products=products,
            products_count={'p1': 1},
        )


def test_order_without_products():
    with pytest.raises(ValidationError):
        Order(
            id=OrderId(uuid.uuid4()),
            user_id=1,
            amount=Money(0),
            is_paid=False,
            delivering=False,
            without_calling=False,
            customer_email=None,
            receiver_name='John',
            receiver_phone_number='+79999999999',
            delivery_address=None,
            delivery_date=datetime.utcnow() + timedelta(days=1),
            delivery_time=None,
            note='',
            cash=False,
            delivery_price=Money(0),
            products=[],
            products_count={},
        )
