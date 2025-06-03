import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter

from apps.pedagog.models.media import Media
from apps.pedagog.models.plan import Plan
from apps.users.models.user import User


class PlanFilter(DropdownFilter):
    title = _("Tematik reja")
    parameter_name = "plan"

    def lookups(self, request, model_admin):
        plans = Plan.objects.all()
        return [
            (
                plan.id,
                f"{plan.science.name} - {plan.science_types.name} - {plan.classes.name} - {plan.class_group.name}",
            )
            for plan in plans
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(plan_id__id=self.value())
        return queryset


# User filter
class UserFilter(DropdownFilter):
    title = _("Foydalanuvchi")
    parameter_name = "user"

    def lookups(self, request, model_admin):
        users = User.objects.all()
        return [
            (
                user.id,
                f"ID:{user.id}-{user.phone} - {user.first_name} {user.last_name} {user.father_name}",
            )
            for user in users
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id__id=self.value())
        return queryset


class MediaFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_user")
    created_at = django_filters.DateFilter(
        field_name="topic__plan_id__created_at", lookup_expr="date"
    )
    quarter = django_filters.CharFilter(method="filter_quarter")
    science = django_filters.CharFilter(method="filter_science")
    science_type = django_filters.CharFilter(method="filter_science_type")
    science_group = django_filters.NumberFilter(
        field_name="topic__plan_id__science__science_grp__id"
    )
    plan_id = django_filters.NumberFilter(field_name="topic__plan_id__id")
    id = django_filters.NumberFilter(field_name="id")
    type = django_filters.CharFilter(field_name="type", lookup_expr="icontains")
    size = django_filters.CharFilter(method="filter_size")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    name = django_filters.CharFilter(method="filter_media_name")
    topic_name = django_filters.CharFilter(method="filter_topic_name")
    classes = django_filters.CharFilter(method="filter_classes")
    classes_type = django_filters.CharFilter(method="filter_classes_type")
    class_group = django_filters.CharFilter(
        method="filter_class_group"
    )  # Filter added here

    class Meta:
        model = Media
        fields = []

    def filter_topic_name(self, queryset, name, value):
        return queryset.filter(topic__name__icontains=value)

    def filter_media_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_user(self, queryset, name, value):
        user_filter = Q()
        for val in value.split(","):
            if val.isdigit():
                user_filter |= Q(topic__user__id=val)
            else:
                user_filter |= Q(user__first_name__icontains=val)
                user_filter |= Q(user__last_name__icontains=val)
        return queryset.filter(user_filter)

    def filter_quarter(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(topic__plan_id__quarter__id=value)
        return queryset.filter(topic__plan_id__quarter__name__icontains=value)

    def filter_science(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(topic__plan_id__science__id=value)
        return queryset.filter(topic__plan_id__science__name__icontains=value)

    def filter_science_type(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(
                Q(topic__plan_id__science_types__id=value)
                | Q(topic__plan_id__science__types__id=value)
            )
        return queryset.filter(
            Q(topic__plan_id__science_types__name__icontains=value)
            | Q(topic__plan_id__science__types__name__icontains=value)
        )

    def human_readable_size(self, size):
        if size is None:
            return "0 B"
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024 ** 2:.2f} MB"
        else:
            return f"{size / 1024 ** 3:.2f} GB"

    def filter_size(self, queryset, name, value):
        # Foydalanuvchi yuborgan qiymat, masalan "1.86"
        # Uni MB, KB, va h.k. qo‘shib taqqoslaymiz
        matched_ids = []

        for obj in queryset:
            human_size = self.human_readable_size(obj.size)
            # Faqat qiymat qismini (masalan 1.86) ajratamiz
            if human_size.startswith(value):
                matched_ids.append(obj.id)

        return queryset.filter(id__in=matched_ids)

    def filter_classes(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(topic__plan_id__classes__id=value)
        return queryset.filter(topic__plan_id__classes__name__icontains=value)

    def filter_classes_type(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(topic__plan_id__classes__type__id=value)
        return queryset.filter(topic__plan_id__classes__type__name__icontains=value)

    def filter_class_group(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(topic__plan_id__class_group__id=value)
        return queryset.filter(topic__plan_id__class_group__name__icontains=value)
