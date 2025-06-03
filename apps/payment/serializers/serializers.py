from rest_framework import serializers

from apps.payment.models.models import Orders, TransactionModel
from apps.pedagog.serializers.moderator import ModeratorListSerializer


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    class Meta:
        fields = (
            "id",
            "start_date",
            "end_date",
            "science",
            "science_language",
            "classes",
            "price",
            "status",
        )
        model = Orders
        extra_kwargs = {
            "start_date": {"read_only": True},
            "end_date": {"read_only": True},
            "price": {"read_only": True},
            "status": {"read_only": True},
        }


class PaymentCreateSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
    status = serializers.BooleanField(read_only=True)


class UzumWebhookSerializer(serializers.Serializer):
    orderId = serializers.CharField()
    bindingId = serializers.CharField()
    orderNumber = serializers.CharField()
    operationType = serializers.CharField()
    operationState = serializers.CharField()


class TransactionSerializer(serializers.ModelSerializer):
    moderator = ModeratorListSerializer()

    class Meta:
        model = TransactionModel
        fields = [
            "id",
            "moderator",
            "transaction_id",
            "status",
            "amount",
            "error",
            "create_at",
        ]
