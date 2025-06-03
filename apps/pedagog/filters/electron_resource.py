import django_filters
from django.db.models import Q

from apps.pedagog.models.electron_resource import ElectronResource


class ElectronResourceFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")  # ID bo‘yicha filter
    user = django_filters.CharFilter(method="filter_user")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    size = django_filters.CharFilter(field_name="size", lookup_expr="icontains")
    type = django_filters.CharFilter(field_name="type", lookup_expr="icontains")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    category = django_filters.NumberFilter(field_name="category__category_id")
    sub_category = django_filters.NumberFilter(field_name="category_id")

    class Meta:
        model = ElectronResource
        fields = []

    def filter_user(self, queryset, name, value):
        try:
            if value.isdigit():
                return queryset.filter(
                    Q(user_id=value)
                    | Q(user__first_name__icontains=value)
                    | Q(user__last_name__icontains=value)
                )
            return queryset.filter(
                Q(user__first_name__icontains=value)
                | Q(user__last_name__icontains=value)
            )
        except:
            return queryset.none()
