# Generated by Django 4.2.11 on 2025-03-01 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0007_alter_order_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="PromoCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=25, verbose_name="Промо-код")),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        verbose_name="Скидка в процентах",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активность"),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="order",
            name="customer_email",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=300,
                null=True,
                verbose_name="Email заказчика",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="done_at",
            field=models.DateTimeField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Время закрытия заказа",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="promo_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="orders",
                to="payments.promocode",
            ),
        ),
    ]
