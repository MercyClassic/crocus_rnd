from pathlib import Path

from django.db.models.signals import post_delete

from products.models import ProductImage


def post_delete_product_image(sender, instance, **kwargs):  # noqa: ARG001
    Path(instance.image.path).unlink()


post_delete.connect(post_delete_product_image, sender=ProductImage)
