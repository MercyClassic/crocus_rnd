import re
from datetime import datetime
from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payments.application.serializers.validators import phone_validator
from payments.db.models import PromoCode


class PaymentCreateSerializer(serializers.Serializer):
    items = serializers.DictField(allow_empty=False)
    amount = serializers.DecimalField(
        max_value=Decimal(1000000),
        max_digits=9,
        decimal_places=2,
    )
    customer_name = serializers.CharField(max_length=150)
    customer_email = serializers.EmailField(max_length=300, allow_blank=True)
    receiver_name = serializers.CharField(max_length=150, allow_blank=True)
    customer_phone_number = serializers.CharField(max_length=20)
    receiver_phone_number = serializers.CharField(max_length=20, allow_blank=True)
    without_calling = serializers.BooleanField()
    delivery_address = serializers.CharField(max_length=200, allow_blank=True)
    delivery_date = serializers.DateTimeField()
    delivery_time = serializers.CharField(max_length=200, allow_blank=True)
    note = serializers.CharField(max_length=300, allow_blank=True)
    cash = serializers.BooleanField()
    delivering = serializers.BooleanField()
    promo_code = serializers.CharField(
        max_length=25, allow_blank=True, required=False,
    )

    def validate_delivery_date(self, value):
        if value.date() < datetime.utcnow().date():
            raise ValidationError
        return value

    def normalize_phone_number(self, phone_number: str) -> str:
        phone_number = re.sub(r'[() -]*', '', phone_number)
        if phone_number[0] != '+':
            phone_number = f'+{phone_number}'
        return f'+7{phone_number[2:]}'

    def validate(self, data):
        phone_fields = [
            ('customer_phone_number', data['customer_phone_number']),
            ('receiver_phone_number', data.get('receiver_phone_number')),
        ]
        for field_name, phone_number in phone_fields:
            if not phone_validator(phone_number or ''):
                raise ValidationError
            data[field_name] = self.normalize_phone_number(phone_number)
        if not data.get('cash') and not data.get('customer_email'):
            raise ValidationError
        return data


class GetPromoCodeDiscountSerializer(serializers.Serializer):
    promo_code = serializers.CharField(max_length=25)
    amount = serializers.DecimalField(
        max_value=Decimal(1000000),
        max_digits=9,
        decimal_places=2,
    )

    def validate(self, data):
        try:
            promo_code = PromoCode.objects.get(
                code=data['promo_code'],
                is_active=True,
            )
        except PromoCode.DoesNotExist as e:
            raise ValidationError from e

        return {
            'promo_code': promo_code.code,
            'value': promo_code.value,
            'amount': (
                data['amount'] * promo_code.get_discount_coefficient(data['amount'])
            ),
        }
