from db.database import async_session_maker
from db.models import Category, Order, OrderProduct, Product, ProductImage
from sqlalchemy import insert, or_, select
from sqlalchemy.orm import joinedload


async def get_paid_orders():
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
            or_(
                Order.is_paid.is_(True),
                Order.cash.is_(True),
            ),
        )
    )
    async with async_session_maker() as session:
        orders = await session.execute(query)
    orders = orders.unique().scalars().all()
    return orders


async def create_product(data: dict) -> tuple:
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
    async with async_session_maker() as session:
        product = await session.execute(stmt)
    product = product.scalar()

    if data['extra_images']:
        product_images = [
            ProductImage(
                image=image,
                product_id=product.id,
            )
            for image in data['extra_image']
        ]
    #     await bulk create
    return product.pk, product.slug


async def create_category(data: dict) -> int:
    stmt = (
        insert(Category)
        .values(
            name=data['name'],
            image=data['image'],
            is_active=data['is_active'],
        )
        .returning(Category.id)
    )
    async with async_session_maker() as session:
        result = await session.execute(stmt)
    return result.scalar().id
