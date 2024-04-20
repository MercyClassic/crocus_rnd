# Generated by Django 4.2.4 on 2023-08-28 22:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0005_alter_order_receiver_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_email',
            field=models.CharField(
                blank=True,
                max_length=300,
                null=True,
                verbose_name='Email заказчика',
            ),
        ),
    ]
