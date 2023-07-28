from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils.validators import phone_validator


class PaymentCreateSerializer(serializers.Serializer):
    items = serializers.DictField(allow_empty=False)
    amount = serializers.IntegerField(max_value=100000)
    customer_name = serializers.CharField(max_length=150)
    receiver_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    customer_phone_number = serializers.CharField(max_length=20)
    receiver_phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    without_calling = serializers.BooleanField()
    delivery_address = serializers.CharField(max_length=200, required=False, allow_blank=True)
    delivery_date = serializers.DateTimeField()
    delivery_time = serializers.CharField(max_length=200, required=False, allow_blank=True)
    note = serializers.CharField(max_length=300, required=False, allow_blank=True)
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
        return data


class CallMeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=12)

    def validate_phone_number(self, value):
        phone = phone_validator(value)
        if not phone:
            raise ValidationError
        return value
