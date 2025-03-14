from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class OrderDTO:
    amount: Decimal
    delivering: bool
    without_calling: bool
    customer_email: str | None
    customer_name: str
    customer_phone_number: str
    receiver_name: str
    receiver_phone_number: str
    delivery_address: str | None
    delivery_date: datetime.utcnow
    delivery_time: str | None
    note: str
    cash: bool
    products: dict
    promo_code: str | None
