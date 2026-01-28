from PIL import Image
from django.db import models
from django.db.models import Manager, QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe


class ProductQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductManager(Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()


class PhotoMixin:
    def thumbnail(self):
        return mark_safe(  # noqa: S308
            f'<img src="{self.image.url}" width = "150" height = "150" '
            'style="object-fit: contain;" />',
        )

    thumbnail.short_description = 'Изображение'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.thumbnail((2000, 1000))
        img.save(self.image.path)


class Product(PhotoMixin, models.Model):
    type_choices = [
        ('bouquet', 'Букет'),
        ('box', 'Коробка'),
        ('basket', 'Корзинка'),
    ]
    title = models.CharField('Название', max_length=128)
    slug = models.SlugField(
        'URL параметр',
        max_length=128,
        unique=True,
        db_index=True,
    )
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    kind = models.CharField(
        'Тип товара',
        max_length=7,
        db_index=True,
        choices=type_choices,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField('В продаже', default=True)
    important = models.IntegerField('Важность', default=1)

    categories = models.ManyToManyField(
        'products.Category',
        through='ProductCategory',
        related_name='products',
    )

    objects = ProductManager()

    class Meta:
        ordering = ['-important', '-id']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title}: {self.price}р'

    def add_to_session(self):
        return reverse('api-add-to-session', kwargs={'slug': self.slug})


class ProductImage(PhotoMixin, models.Model):
    image = models.ImageField('Изображение', upload_to='images/')
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='images',
    )

    class Meta:
        verbose_name = 'Дополнительное изоражение'
        verbose_name_plural = 'Дополнительные изоражения'

    def __str__(self):
        return f'{self.image}'


class ProductCategory(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.product.title} - {self.category.name}'


class Category(PhotoMixin, models.Model):
    image = models.ImageField('Изображение', upload_to='images/')
    name = models.CharField('Название', max_length=50, db_index=True)
    is_active = models.BooleanField('Активно', default=True)
    important = models.IntegerField('Важность', default=1)

    class Meta:
        ordering = ['-important', '-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} - {self.image}'
