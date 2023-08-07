import uuid

from django.db import models

from accounts.models import phone_regex


class Order(models.Model):
    uuid = models.UUIDField(
        'uuid',
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        'accounts.Account',
        editable=False,
        on_delete=models.DO_NOTHING,
        related_name='products',
    )
    amount = models.IntegerField('Всего')
    is_paid = models.BooleanField('Оплачено', default=False)
    delivering = models.BooleanField('С доставкой', default=False)
    created_at = models.DateTimeField('Время создания заказа', auto_now_add=True)
    done_at = models.DateTimeField('Время закрытия заказа', blank=True, null=True)

    without_calling = models.BooleanField('Писать в телеграм/ватсап', default=False)
    receiver_name = models.CharField(
        'Имя получателя',
        max_length=50,
        blank=True,
        null=True,
        default='Заказчик является получаетелем',
    )
    receiver_phone_number = models.CharField(
        'Номер телефона получателя',
        max_length=50,
        validators=[phone_regex],
        blank=True,
        null=True,
        default='Заказчик является получаетелем',
    )
    delivery_address = models.CharField(
        'Адрес доставки',
        max_length=200,
        blank=True,
        null=True,
        default='Без доставки',
    )
    delivery_date = models.DateTimeField('Дата доставки/самовывоза')
    delivery_time = models.CharField(
        'Время доставки',
        max_length=200,
        blank=True,
        null=True,
        default='Без доставки',
    )
    note = models.CharField(
        'Примечание',
        max_length=300,
        blank=True,
        null=True,
        default='Без примечания',
    )
    cash = models.BooleanField(
        'Оплата наличными',
        default=False,
    )

    products = models.ManyToManyField(
        'products.Product',
        through='OrderProduct',
        related_name='orders',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk}'

    def save(self, *args, **kwargs):
        field_names = (
            'receiver_name',
            'receiver_phone_number',
            'delivery_address',
            'delivery_time',
            'note',
        )
        for field_name in field_names:
            if getattr(self, field_name) in ['', None]:
                setattr(self, field_name, self._meta.get_field(field_name).default)
        return super().save(*args, **kwargs)


class OrderProduct(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.DO_NOTHING,
        verbose_name='Товар',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        verbose_name='Заказ',
    )
    count = models.IntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def __str__(self):
        return f'Продукта заказа #{self.order_id}'
