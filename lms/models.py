from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course/photo", **NULLABLE, verbose_name="Изображение"
    )
    description = models.CharField(max_length=100, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.SET_NULL, **NULLABLE
    )
    title = models.CharField(
        max_length=255, verbose_name="Название урока", help_text="Lesson Title"
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Lesson Description"
    )
    preview = models.ImageField(
        upload_to="lms/lessons",
        verbose_name="Превью урока",
        help_text="Lessons Preview",
        **NULLABLE
    )
    video_url = models.URLField(
        verbose_name="Ссылка на урок", help_text="Video URL", **NULLABLE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["course", "title"]
