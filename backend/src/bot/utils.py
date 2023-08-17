import os

from asgiref.sync import sync_to_async

from bot.handlers.others import unknown_command
from products.models import Product, ProductImage, Category

admin_ids = [int(admin_id) for admin_id in os.getenv('ADMIN_TG_BOT_IDS').split(', ')]
owner_ids = [int(owner_id) for owner_id in os.getenv('OWNER_TG_BOT_IDS').split(', ')]


def command_for(permission_level: str):
    def decorator(func):
        def wrapper(*args):
            message = args[0]
            if (
                    (permission_level == 'admin' and message.from_user.id in admin_ids)
                    or (permission_level == 'owner' and message.from_user.id in owner_ids)
            ):
                return func(*args)
            return unknown_command(message)
        return wrapper
    return decorator


async def create_product(data: dict) -> tuple:
    product = await Product.objects.acreate(
        title=data['title'],
        slug=data['slug'],
        description=data['description'],
        price=data['price'],
        kind=data['kind'],
        image=data['image'],
    )
    product_images = []
    if data['extra_images']:
        for image in data['extra_images']:
            product_images.append(ProductImage(image=image, product=product))
        await sync_to_async(ProductImage.objects.bulk_create)(product_images)
    return product.pk, product.slug


async def create_category(data: dict) -> int:
    category = await Category.objects.acreate(
        name=data['name'],
        image=data['image'],
        is_active=data['is_active'],
    )
    return category.pk


def slugify_string(string: str) -> str:
    return string.translate(
        str.maketrans(
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ’',
            'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA__',
        ),
    )


def validate_title(title: str) -> bool:
    forbidden_characters = '!@#$%^&*()+=`~;:"[]{}.,\'\\/'
    for char in title:
        if char in forbidden_characters:
            return False
    return True
