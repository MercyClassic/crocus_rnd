import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


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
    amount = models.DecimalField('Всего', max_digits=7, decimal_places=2)
    is_paid = models.BooleanField('Оплачено', default=False)
    delivering = models.BooleanField('С доставкой', default=False)
    created_at = models.DateTimeField('Время создания заказа', auto_now_add=True)
    done_at = models.DateTimeField(
        'Время закрытия заказа',
        default=None,
        blank=True,
        null=True,
    )
    without_calling = models.BooleanField('Писать в телеграм/ватсап', default=False)
    customer_email = models.CharField(
        'Email заказчика',
        max_length=300,
        default=None,
        blank=True,
        null=True,
    )
    receiver_name = models.CharField(
        'Имя получателя',
        max_length=200,
        blank=True,
        null=True,
        default='Заказчик является получаетелем',
    )
    receiver_phone_number = models.CharField(
        'Номер телефона получателя',
        max_length=30,
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
    promo_code = models.ForeignKey(
        'payments.PromoCode',
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk}'


class OrderProduct(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.DO_NOTHING,
        verbose_name='Товар',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name='order_products',
        verbose_name='Заказ',
    )
    count = models.IntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def __str__(self):
        return f'Продукта заказа #{self.order_id}'


class PromoCode(models.Model):
    code = models.CharField(max_length=25, verbose_name='Промо-код', unique=True)
    value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Значение скидки',
    )
    is_percent = models.BooleanField(
        default=False,
        verbose_name='Скидка указана в процентах',
    )
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'Промо код'
        verbose_name_plural = 'Промо коды'

    def __str__(self):
        return (
            f'Промокод: {self.code} ({self.value}'
            f'{"%" if self.is_percent else "руб"})'
        )

    def clean(self):
        super().clean()
        if self.is_percent and self.value > 100:
            raise ValidationError(
                {'value': 'Процентная скидка не может быть больше 100%!'},
            )

    def get_discount_coefficient(self, amount: Decimal | int):
        if self.is_percent:
            return Decimal(1 - self.value / 100)
        else:
            return Decimal(1 - self.value / amount)
