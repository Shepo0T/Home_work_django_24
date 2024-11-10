from django.contrib import admin

from lms.models import Subscription
from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "User" в административной панели"""

    list_display = (
        "pk",
        "email",
    )


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Payment" в административной панели"""

    list_display = (
        "pk",
        "user",
        "payment_course",
        "payment_lesson",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course',)