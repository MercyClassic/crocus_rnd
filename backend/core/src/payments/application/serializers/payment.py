from datetime import datetime
from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payments.application.validators import phone_validator


class PaymentCreateSerializer(serializers.Serializer):
    items = serializers.DictField(allow_empty=False)
    amount = serializers.DecimalField(
        max_value=Decimal(1000000), max_digits=9, decimal_places=2
    )
    customer_name = serializers.CharField(max_length=150)
    customer_email = serializers.CharField(max_length=300, allow_blank=True)
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

    def validate_delivery_date(self, value):
        if value.date() < datetime.utcnow().date():
            raise ValidationError
        return value

    def validate(self, data):
        phone_numbers = [data.get('customer_phone_number')]
        receiver_phone_number = data.get('receiver_phone_number')
        if receiver_phone_number:
            phone_numbers.append(receiver_phone_number)
        for value in phone_numbers:
            phone = phone_validator(value)
            if not phone:
                raise ValidationError
        if not data.get('cash') and not data.get('customer_email'):
            raise ValidationError
        return data
