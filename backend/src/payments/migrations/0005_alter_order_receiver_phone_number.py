# Generated by Django 4.2.4 on 2023-08-20 23:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0004_alter_order_receiver_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receiver_phone_number',
            field=models.CharField(
                blank=True,
                default='Заказчик является получаетелем',
                max_length=30,
                null=True,
                verbose_name='Номер телефона получателя',
            ),
        ),
    ]