from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductData:
    title: str
    count: int


@dataclass
class OrderData:
    id: int
    amount: int
    delivering: bool
    created_at: datetime.utcnow
    without_calling: bool
    delivery_address: str
    delivery_date: datetime.utcnow
    delivery_time: str
    note: str
    cash: bool
    products: list | dict

    def __post_init__(self):
        self.created_at = self.created_at.strftime('%d.%m.%Y %H:%M')
        self.delivery_date = self.delivery_date.strftime('%d.%m.%Y')
        products = []
        for key, value in self.products.items():
            products.append(ProductData(title=key, count=value))
        self.products = products
