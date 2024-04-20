# Generated by Django 4.1.10 on 2023-07-17 18:56

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name='uuid',
                    ),
                ),
                ('amount', models.IntegerField(verbose_name='Всего')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('delivering', models.BooleanField(default=False, verbose_name='С доставкой')),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='Время создания заказа'),
                ),
                (
                    'done_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name='Время закрытия заказа',
                    ),
                ),
                (
                    'without_calling',
                    models.BooleanField(default=False, verbose_name='Писать в телеграм/ватсап'),
                ),
                (
                    'receiver_name',
                    models.CharField(
                        blank=True,
                        default='Заказчик является получаетелем',
                        max_length=50,
                        null=True,
                        verbose_name='Имя получателя',
                    ),
                ),
                (
                    'receiver_phone_number',
                    models.CharField(
                        blank=True,
                        default='Заказчик является получаетелем',
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message='Номер должен начинаться с +7 и состоять из 11 цифр',
                                regex='^+7\\d{10}$',
                            ),
                        ],
                        verbose_name='Номер телефона получателя',
                    ),
                ),
                (
                    'delivery_address',
                    models.CharField(
                        blank=True,
                        default='Без доставки',
                        max_length=200,
                        null=True,
                        verbose_name='Адрес доставки',
                    ),
                ),
                ('delivery_date', models.DateTimeField(verbose_name='Дата доставки/самовывоза')),
                (
                    'delivery_time',
                    models.CharField(
                        blank=True,
                        default='Без доставки',
                        max_length=200,
                        null=True,
                        verbose_name='Время доставки',
                    ),
                ),
                (
                    'note',
                    models.CharField(
                        blank=True,
                        default='Без примечания',
                        max_length=200,
                        null=True,
                        verbose_name='Примечание',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('count', models.IntegerField(default=1, verbose_name='Количество')),
                (
                    'order',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='payments.order',
                        verbose_name='Заказ',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='products.product',
                        verbose_name='Товар',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Товар заказа',
                'verbose_name_plural': 'Товары заказов',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(
                related_name='orders',
                through='payments.OrderProduct',
                to='products.product',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='products',
                to='accounts.account',
            ),
        ),
    ]