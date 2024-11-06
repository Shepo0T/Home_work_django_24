from django.contrib.auth.models import AbstractUser

from django.db import models

from lms.models import Course, Lesson

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


class Payments(models.Model):

    CASH = "cash"
    ONLINE = "online"
    PAYMENT_METHOD = [(CASH, "cash"), (ONLINE, "online")]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="За кого произведена оплата"
    )
    payment_date = models.DateField(verbose_name="Дата платежа", **NULLABLE)
    payment_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    payment_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )
    cost = models.PositiveIntegerField(default=0, verbose_name="Стоимость покупки")
    payment_method = models.CharField(
        choices=PAYMENT_METHOD, default=CASH, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return self.payment_method
