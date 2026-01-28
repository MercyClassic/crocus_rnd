from dataclasses import dataclass
from datetime import datetime

from payments.domain.entities.value_objects import Money


@dataclass
class OrderDTO:
    amount: Money
    delivering: bool
    without_calling: bool
    customer_email: str | None
    customer_name: str
    customer_phone_number: str
    receiver_name: str
    receiver_phone_number: str
    delivery_address: str | None
    delivery_date: datetime
    delivery_time: str | None
    note: str
    cash: bool
    products: dict[str, int]
    promo_code: str | None
