from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=CHOICES,
        default=CHOICES[0][0]
    )
    confirmation_code = models.CharField(max_length=16, blank=True)

    REQUIRED_FIELDS = ['email']
