from django.urls import path
from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
    LessonDestroyAPIView,
)

app_name = LmsConfig.name
router = DefaultRouter()

router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="list_lesson"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="create_lesson"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="update_lesson"
    ),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="one_lesson"),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="delete_lesson"
    ),
] + router.urls
