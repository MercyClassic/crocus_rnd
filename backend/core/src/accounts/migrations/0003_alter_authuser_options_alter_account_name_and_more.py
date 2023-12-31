# Generated by Django 4.2.3 on 2023-07-27 15:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_authuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authuser',
            options={'verbose_name': 'Администратор', 'verbose_name_plural': 'Администраторы'},
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(
                error_messages={'unique': 'Пользователь с таким номером телефона уже существует'},
                max_length=20,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message='Номер должен начинаться с +7 и состоять из 11 цифр',
                        regex='^+7\\d{10}$',
                    ),
                ],
                verbose_name='Телефон',
            ),
        ),
    ]
