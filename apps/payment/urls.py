from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payment.views.views import (
    PaymentViewSet,
    OrderViewSet,
    WebhookApiView,
    TransactionViewSet,
)

router = DefaultRouter()
router.register("payment", PaymentViewSet, basename="payments")
router.register("orders", OrderViewSet, basename="order")
router.register("webhook", WebhookApiView, basename="webhook")
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [path("", include(router.urls))]
