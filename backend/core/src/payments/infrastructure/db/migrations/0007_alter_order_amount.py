# Generated by Django 4.2.5 on 2023-10-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0006_order_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Всего'),
        ),
    ]