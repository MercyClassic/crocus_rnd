from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class ProductData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str


class ProductAssociationSchema(BaseModel):
    count: int
    model_config = ConfigDict(from_attributes=True)
    product: ProductData


class OrderData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: int
    delivering: bool
    created_at: datetime
    without_calling: bool
    delivery_address: str
    delivery_date: datetime
    delivery_time: str
    note: str
    cash: bool
    product_associations: List[ProductAssociationSchema]

    @field_validator('created_at')
    def pre_validate_created_at(cls, value):
        return (value + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

    @field_validator('delivery_date')
    def pre_validate_delivery_date(cls, value):
        return (value + timedelta(hours=3)).strftime('%d-%m-%Y')
