from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import UserSerializers, PaymentSerializer

from users.models import User, Payments
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания пользователя"""
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class UserListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка пользователей"""
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра одного пользователя"""
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования пользователя"""
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

class PaymentCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания платежей"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        """Переопределение метода для возможности оплаты курсов."""
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        price_id = create_stripe_price(payment, stripe_product_id)
        session_id, session_link = create_stripe_session(price_id)
        payment.session_id = session_id
        payment.payment_link = session_link
        payment.save()

class PaymentListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "payment_method",
        "payment_course",
        "payment_lesson",
    )
    ordering_fields = ("date",)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра одного платежа"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования платежа"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()