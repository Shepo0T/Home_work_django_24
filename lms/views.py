from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class =CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name="moderators"):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.pk)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated & ~IsModerator,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (
                IsAuthenticated & IsOwner | IsModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated & IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModerator,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name="moderators"):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.pk)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwner,)

class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        sub_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
        return Response({"message": message})