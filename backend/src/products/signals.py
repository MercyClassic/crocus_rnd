import os

from django.db.models.signals import post_delete

from products.models import ProductImage


def post_delete_product_image(sender, instance, **kwargs):
    os.remove(instance.image.path)


post_delete.connect(post_delete_product_image, sender=ProductImage)
