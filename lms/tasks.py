from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from lms.models import Course, Subscription


@shared_task
def send_email_updating_course(course_pk):
    """Функция отправки сообщения об обновлении курса подписчикам."""
    course = get_object_or_404(Course, pk=course_pk)
    subs = Subscription.objects.filter(course=course.pk)
    if subs:
        print("Рассылка запущена")
        send_mail(
            subject=f"Обновление курса {course.title}",
            message=f"Здравствуйте! Курс {course.title} обновлен! Скорее посмотрите, что изменилось!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sub.user.email for sub in subs],
        )
        print("Рассылка завершена")