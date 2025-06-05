from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from apps.payment.models.models import Orders, Payments, TransactionModel
from apps.payment.serializers.serializers import (
    OrderSerializer,
    PaymentCreateSerializer,
    UzumWebhookSerializer,
    TransactionSerializer,
)
from apps.payment.services.services import UzumService
from apps.shared.pagination.custom import CustomPagination
from apps.shared.utils.logger import logger


class OrderViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        user = self.request.user
        science = serializer.validated_data.get("science")
        science_language = serializer.validated_data.get("science_language")
        classes = serializer.validated_data.get("classes")
        current_date = timezone.now().date()

        if Orders.objects.filter(
            user=user,
            science=science,
            science_language=science_language,
            classes=classes,
            start_date__lte=current_date,
            end_date__gte=current_date,
            status=True,
        ).exists():
            raise APIException(
                _("Bu foydalanuvchi uchun bu turdagi buyurtma allaqachon mavjud.")
            )

        return serializer.save(user=user)

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user).order_by("-id")


class PaymentViewSet(ViewSet):
    serializer_class = PaymentCreateSerializer

    @action(detail=False, methods=["POST"], url_path="create")
    def create_payment(self, request):
        try:
            ser = self.serializer_class(data=request.data)
            ser.is_valid(raise_exception=True)
            data = ser.validated_data
            order = data.get("order")

            trans_id, redirect_url = UzumService().generate_link(
                request.user.id,
                order.id,
                order.price,
                f"To'lov miqdori {order.price}, to'lov sanasi {order.created_at.strftime('%d-%m-%Y')}, "
                f"to'lov buyurtma raqami {order.id}, buyurtma {order.science}",
            )
            Payments.objects.get_or_create(
                order=order, price=order.price, trans_id=trans_id
            )
            return Response(
                {
                    "detail": _("Payment created"),
                    "data": {"url": redirect_url},
                }
            )
        except Exception as e:
            import traceback

            print("Error:", e)
            print(traceback.format_exc())
            raise APIException(str(e))


class WebhookApiView(ViewSet):
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["POST", "GET"],
        url_name="uzum-webhook",
        url_path="uzum",
    )
    def uzum(self, request):
        ser = UzumWebhookSerializer(data=request.data)
        ser.is_valid()
        data = ser.data
        if data.get("operationState") != "SUCCESS":
            logger.error(ser.errors)
            return Response({"success": False})
        payment = Payments.objects.filter(trans_id=data.get("orderId"))
        if not payment.exists():
            logger.error("Order not found: {}".format(data.get("orderId")))
            return Response({"success": False})
        payment = payment.first()
        order = payment.order
        payment.status = True
        order.status = True
        payment.save()
        order.save()
        logger.debug("Payment success: {}".format(data.get("orderNumber")))
        return Response({"success": True})


class TransactionViewSet(ViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request):
        transactions = TransactionModel.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<moderator_id>\d+)")
    def moderator_transactions(self, request, moderator_id=None):
        transactions = TransactionModel.objects.filter(moderator_id=moderator_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"me")
    def my_transactions(self, request):
        transactions = TransactionModel.objects.filter(moderator__user=request.user)
        paginator = CustomPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(
            paginated_transactions, many=True
        )
        return paginator.get_paginated_response(serializer.data)
