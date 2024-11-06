from rest_framework import serializers

from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    payments_history = PaymentSerializer(
        many=True, source="payment_set", read_only=True
    )

    class Meta:
        model = User
        fields = "__all__"
