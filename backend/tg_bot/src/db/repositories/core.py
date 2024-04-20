from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models import Order, OrderProduct
from db.models.products import Category, Product, ProductImage


class CoreRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_paid_orders(self):
        query = (
            select(Order)
            .options(
                joinedload(Order.product_associations)
                .load_only(OrderProduct.count)
                .options(
                    joinedload(OrderProduct.product).load_only(Product.title),
                ),
            )
            .where(
                Order.done_at.is_(None),
            )
        )
        orders = await self._session.execute(query)
        return orders.unique().scalars().all()

    async def get_order(self, order_id: int) -> Order | None:
        query = (
            select(Order)
            .options(
                joinedload(Order.product_associations)
                .load_only(OrderProduct.count)
                .options(
                    joinedload(OrderProduct.product).load_only(Product.title),
                ),
            )
            .where(
                Order.id == order_id,
            )
        )
        order = await self._session.execute(query)
        return order.scalar()

    async def create_product(self, data: dict) -> tuple:
        stmt = (
            insert(Product)
            .values(
                title=data['title'],
                slug=data['slug'],
                description=data['description'],
                price=data['price'],
                kind=data['kind'],
                image=data['image'],
            )
            .returning(Product)
        )
        product = await self._session.execute(stmt)
        product = product.scalar()

        if data['extra_images']:
            product_images = [
                {
                    'image': image,
                    'product_id': product.id,
                }
                for image in data['extra_images']
            ]

            stmt = insert(ProductImage).values(product_images)
            await self._session.execute(stmt)
        await self._session.commit()

        return product.id, product.slug

    async def create_category(self, data: dict) -> int:
        stmt = (
            insert(Category)
            .values(
                name=data['name'],
                image=data['image'],
                is_active=data['is_active'],
            )
            .returning(Category.id)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar()
