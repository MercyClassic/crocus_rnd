from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payments.application.serializers.validators import phone_validator


class CallMeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=12)

    def validate_phone_number(self, value):
        phone = phone_validator(value)
        if not phone:
            raise ValidationError
        return value
