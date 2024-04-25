from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import (
    DATETIME,
    UUID,
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.products import Product


class Order(Base):
    __tablename__ = 'payments_order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[uuid4] = mapped_column(UUID, unique=True, index=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[str] = mapped_column(Numeric(7, 2))
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    delivering: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), default=datetime.now)
    done_at: Mapped[datetime] = mapped_column(DATETIME(timezone=True), nullable=True)
    without_calling: Mapped[bool] = mapped_column(Boolean, default=False)
    customer_email: Mapped[str] = mapped_column(String(300), nullable=True)
    receiver_name: Mapped[str] = mapped_column(String(200), nullable=True)
    receiver_phone_number: Mapped[str] = mapped_column(String(30), nullable=True)
    delivery_address: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        default='Без доставки',
    )
    delivery_date: Mapped[datetime] = mapped_column(DATETIME)
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
    product_associations: Mapped[list['OrderProduct']] = relationship(back_populates='order')


class OrderProduct(Base):
    __tablename__ = 'payments_orderproduct'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products_product.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('payments_order.id'))
    product: Mapped['Product'] = relationship(back_populates='order_associations')
    order: Mapped['Order'] = relationship(back_populates='product_associations')
    count: Mapped[int] = mapped_column(Integer, default=1)
