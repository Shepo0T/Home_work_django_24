from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            LinkValidator(field='video_url')
        ]

class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_subscription(self, course):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"
class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'