from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ProductDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str


class ProductAssociationDTO(BaseModel):
    count: int
    model_config = ConfigDict(from_attributes=True)
    product: ProductDTO


class OrderDTO(BaseModel):
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
    product_associations: list[ProductAssociationDTO]

    @field_validator('created_at')
    @classmethod
    def pre_validate_created_at(cls, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @field_validator('delivery_date')
    @classmethod
    def pre_validate_delivery_date(cls, value):
        return value.strftime('%d-%m-%Y')
