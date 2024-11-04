from django.contrib.auth.models import AbstractUser

from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(
        max_length=25, verbose_name="Телефон", **NULLABLE, help_text="Укажите номер"
    )
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    country = models.CharField(
        max_length=20, verbose_name="Страна", **NULLABLE, help_text="Укажите страну"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
