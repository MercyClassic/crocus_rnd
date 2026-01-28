from collections.abc import Iterable

from products.db.models import Product as ProductModel


class ProductRepository:
    def list(self, products_slug: Iterable[str]):
        return ProductModel.objects.only('title', 'slug', 'price').filter(
            slug__in=[*products_slug],
        )
