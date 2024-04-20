from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.payments import OrderProduct


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
    important: Mapped[int] = mapped_column(Integer, default=1)

    order_associations: Mapped[list['OrderProduct']] = relationship(back_populates='product')

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
    important: Mapped[int] = mapped_column(Integer, default=1)
