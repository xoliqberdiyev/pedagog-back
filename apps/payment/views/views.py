from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

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
from rest_framework.views import APIView

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
from apps.payment.services.payment import PaymentService
from apps.users.models.user import SourceChoice
from apps.pedagog.models.electron_resource import ElectronResource


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
        
        header_source = self.request.headers.get("source")
        if header_source in SourceChoice.values:
            source = header_source
        else:
            source = SourceChoice.BOT

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
            
        end_date = current_date + timedelta(days=30) 

        return serializer.save(user=user, source=source, end_date=end_date)
    
    def get_queryset(self):
        queryset = Orders.objects.filter(user=self.request.user).order_by("-id")
        is_paid = self.request.query_params.get("is_paid")

        if is_paid is not None:
            is_paid_bool = str(is_paid).lower() == "true"
            queryset = queryset.filter(status=is_paid_bool)

        return queryset


class PaymentViewSet(ViewSet):
    serializer_class = PaymentCreateSerializer

    @action(detail=False, methods=["POST"], url_path="create")
    def create_payment(self, request):
        try:
            ser = self.serializer_class(data=request.data)
            ser.is_valid(raise_exception=True)
            data = ser.validated_data
            order = data.get("order")
            payment_type = data.get("payment_type")
            
            user_id = request.user.id
            payment_services = PaymentService(user_id)
            trans_id, pay_link = payment_services.generate_link(order, payment_type)
            Payments.objects.get_or_create(
                order=order, price=order.price, trans_id=trans_id
            )   
            return Response(
                {
                    "detail": _("Payment created"),
                    "data": {"url": pay_link},
                }
            )
        except Exception as e:
            import traceback

            print("Error:", e)
            print(traceback.format_exc())
            raise APIException(f"error: {str(e)} ")


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
        paginator = CustomPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<moderator_id>\d+)")
    def moderator_transactions(self, request, moderator_id=None):
        transactions = TransactionModel.objects.filter(moderator_id=moderator_id)
        paginator = CustomPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"me")
    def my_transactions(self, request):
        transactions = TransactionModel.objects.filter(moderator__user=request.user)
        paginator = CustomPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)


class PaymentCreateViaClickApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order')
        if not order_id:
            return Response(
                {
                    'detail': 'Order field required',
                }, status=400
            )
        order = get_object_or_404(Orders, id=order_id)
        user_id = request.user.id
        payment_services = PaymentService(user_id)
        trans_id, pay_link = payment_services.generate_link(order, 'click_2')
        Payments.objects.get_or_create(
            order=order, price=order.price, trans_id=trans_id
        )
        return Response(
            {
                "detail": _("Payment created"),
                "data": {"url": pay_link},
            }
        )


class PayToElectronicResourceApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        resource = get_object_or_404(ElectronResource, id=id)
        if resource.price is None:
            return Response(
                {
                    'success': False,
                    'message': 'Resurs bepul',
                }, status=400
            )
        payment_type = request.data.get('payment_type')
        if not payment_type and not payment_type in ['click', 'payme', 'click_2']:
            return Response(
                {
                    'success': False,
                    'error': 'payment_type field is required and choiches -> click, payme, click_2'
                }, status=400
            )
        current_date = timezone.now().date()
        order, created = Orders.objects.get_or_create(
            user=request.user,
            electronic_resource=resource,
            price=resource.price,
            start_date__lte=current_date,
            end_date__gte=current_date,
            status=True,
        )

        if created:
            logger.info(f"Order created")
        payment_services = PaymentService(request.user.id)
        trans_id, pay_link = payment_services.generate_link(order, payment_type)
        Payments.objects.get_or_create(
            order=order,
            price=order.price,
            trans_id=trans_id,
        )
        return Response(
            {
                'success': True,
                'pay_link': pay_link
            }, status=200
        )