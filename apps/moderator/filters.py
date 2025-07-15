import django_filters
from apps.moderator.models.permission import ModeratorPermission


class ModeratorPermissionFilter(django_filters.FilterSet):
    class Meta:
        model = ModeratorPermission
        fields = {
            "status": ["exact"],
            "school_type": ["exact"],
            "classes": ["exact"],
            "science": ["exact"],
            "science_language": ["exact"],
            "user": ["exact"],
        }
