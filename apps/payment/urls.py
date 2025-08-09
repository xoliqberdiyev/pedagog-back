from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payment.views.views import (
    PaymentViewSet,
    OrderViewSet,
    WebhookApiView,
    TransactionViewSet,
)
from apps.payment.views.click import ClickWebhookAPIView
from apps.payment.views.payme import PaymeCallBackAPIView


router = DefaultRouter()
router.register("payment", PaymentViewSet, basename="payments")
router.register("orders", OrderViewSet, basename="order")
router.register("webhook", WebhookApiView, basename="webhook")
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
    path("payment/click/update/", ClickWebhookAPIView.as_view()),
    path("payment/update/", PaymeCallBackAPIView.as_view()),

]
