# Generated by Django 4.2.3 on 2023-08-07 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_order_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cash',
            field=models.BooleanField(default=False, verbose_name='Оплата наличными'),
        ),
    ]
