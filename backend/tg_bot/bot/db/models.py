from datetime import datetime
from typing import List
from uuid import uuid4

from db.database import Base
from sqlalchemy import (
    DATETIME,
    UUID,
    Boolean,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    __tablename__ = 'products_product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    image: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(Numeric(8, 2))
    kind: Mapped[str] = mapped_column(String(10), index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    important: Mapped[bool] = mapped_column(Boolean, default=1)

    order_associations: Mapped[List['OrderProduct']] = relationship(back_populates='product')

    def __repr__(self):
        return f'{self.id} - {self.title}'


class ProductImage(Base):
    __tablename__ = 'products_productimage'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String(128))
    product_id: Mapped[int] = mapped_column(ForeignKey('products_product.id'))


class Category(Base):
    __tablename__ = 'products_category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(50), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    important: Mapped[bool] = mapped_column(Boolean, default=1)


class Order(Base):
    __tablename__ = 'payments_order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[uuid4] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[str] = mapped_column(Numeric(7, 2))
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    delivering: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow())
    done_at: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    without_calling: Mapped[bool] = mapped_column(Boolean, default=False)
    customer_email: Mapped[str] = mapped_column(String(300), nullable=True)
    receiver_name: Mapped[str] = mapped_column(String(200), nullable=True)
    receiver_phone_number: Mapped[str] = mapped_column(String(30), nullable=True)
    delivery_address: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        default='Без доставки',
    )
    delivery_date: Mapped[Date] = mapped_column(Date)
    delivery_time: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        default='Без доставки',
    )
    note: Mapped[str] = mapped_column(
        String(300),
        nullable=True,
        default='Без примечания',
    )
    cash: Mapped[bool] = mapped_column(Boolean, default=False)
    product_associations: Mapped[List['OrderProduct']] = relationship(back_populates='order')


class OrderProduct(Base):
    __tablename__ = 'payments_orderproduct'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products_product.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('payments_order.id'))
    product: Mapped['Product'] = relationship(back_populates='order_associations')
    order: Mapped['Order'] = relationship(back_populates='product_associations')
    count: Mapped[int] = mapped_column(Integer, default=1)
