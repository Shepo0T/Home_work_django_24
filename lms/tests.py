from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@example.com')
        self.course = Course.objects.create(title='course_test', description='course_test', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson_test', description='lesson_test', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        url = reverse('lms:course-list')
        data = {
            'title': 'course_test',
            'description': 'course_test'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {
            'title': 'Python'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Python'
        )

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))

        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        print(response.json())
        data = response.json()
        result = {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
            'id': 4,
            'lessons':[
                {
                    'id': 3,
                    'title': 'lesson_test',
                    'description': 'lesson_test',
                    'preview': None,
                    'video_url': None,
                    'course': 4,
                    'owner': 3
                }
                ],
            'title': 'course_test',
            'preview': None,
            'description': 'course_test',
            'owner': 3
        }
                ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )



class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@project.test', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(title='course_test', description='course_test', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson_test', description='lesson_test', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:one_lesson', args=(self.lesson.pk,))
        response = self.client.get(url)
        print(response.json())
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('lms:create_lesson')
        data = {
            'title': 'lesson_test',
            'description': 'lesson_test'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('lms:update_lesson', args=(self.lesson.pk,))
        data = {
            'title': 'Python'
        }
        response = self.client.patch(url, data)
        print((response.json()))
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Python'
        )

    def test_lesson_delete(self):
        url = reverse('lms:delete_lesson', args=(self.lesson.pk,))

        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('lms:list_lesson')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@project.test', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(title='course_test', description='course_test', owner=self.user)
        self.lesson = Lesson.objects.create(title='lesson_test', description='lesson_test', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('lms:subscription')
        data = {
            'user': self.user,
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, {'message': 'Подписка добавлена'}
        )

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('lms:subscription')
        data = {
            'user': self.user,
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, {'message': 'Подписка удалена'}
        )
