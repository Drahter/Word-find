from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Никнейм пользователя'
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    avatar = models.ImageField(
        upload_to='users/users_avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    country = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Страна'
    )

    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='ID чата в телеграме'
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
