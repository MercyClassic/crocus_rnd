from django.contrib.auth.models import AbstractUser
from django.db import models


class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return f'{self.email}'


class Account(models.Model):
    phone_number = models.CharField(
        'Телефон',
        unique=True,
        max_length=12,
        error_messages={'unique': 'Пользователь с таким номером телефона уже существует'},
    )
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'{self.name}: {self.phone_number}'
