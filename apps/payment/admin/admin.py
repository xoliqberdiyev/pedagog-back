from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from apps.payment.models.models import (
    PlansRequirements,
    TransactionModel,
    Orders,
    Payments,
    Plans,
)


class PlansRequirementsInline(StackedInline):
    model = PlansRequirements
    extra = 0
    tab = True


@admin.register(PlansRequirements)
class PlansRequirementsAdmin(ModelAdmin):
    list_display = ("id", "plan", "name")
    search_fields = ("name",)
    list_filter = ("plan__quarter__name",)


@admin.register(TransactionModel)
class TransactionModelAdmin(ModelAdmin):
    list_display = ["transaction_id", "status", "error", "moderator"]
    list_filter = [
        "status",
        "moderator__user__first_name",
        "moderator__user__last_name",
        "moderator__user__phone",
    ]


@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "price",
        "start_date",
        "created_at",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    list_filter = ("status",)
    autocomplete_fields = ("user", "classes", "science", "science_language")


@admin.register(Payments)
class PaymentsAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "price",
        "status",
        "trans_id",
    )
    search_fields = (
        "order__user__first_name",
        "order__user__last_name",
        "order__user__phone",
        "order__plan__name",
        "trans_id",
    )
    list_filter = ("status",)


@admin.register(Plans)
class PlansAdmin(ModelAdmin):
    list_display = (
        "id",
        "quarter",
        "price",
    )
    search_fields = ("price",)
    ordering = ("quarter",)
    autocomplete_fields = ("quarter",)
    list_filter = ("quarter",)
    inlines = [PlansRequirementsInline]
