# Generated by Django 4.2.4 on 2023-08-21 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0002_rename_type_product_kind'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={
                'ordering': ['-id', '-important'],
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='important',
            field=models.IntegerField(default=1, verbose_name='Важность'),
        ),
    ]
