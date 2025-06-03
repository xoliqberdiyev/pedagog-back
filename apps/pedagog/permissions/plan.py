from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from apps.pedagog.models.moderator import Moderator


class PlanPermission(permissions.BasePermission):
    message = _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")

    def __init__(self, roles: list) -> None:
        super().__init__()
        self.roles = roles

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        user = request.user
        try:
            science = int(request.data.get("science"))
            science_type = int(request.data.get("science_types"))
            classes = int(request.data.get("classes"))
            class_groups = int(request.data.get("class_group"))
            quarters = int(request.data.get("quarter"))
        except (TypeError, ValueError):
            raise ValidationError("Invalid data provided.")

        try:
            moderator = Moderator.objects.get(user=user)
            if (
                not moderator.plan_creatable
                or not moderator.science.filter(id=science).exists()
                or not moderator.science_type.filter(id=science_type).exists()
                or not moderator.classes.filter(id=classes).exists()
                or not moderator.class_groups.filter(id=class_groups).exists()
                or not moderator.quarters.filter(id=quarters).exists()
            ):
                raise ValidationError("User is not allowed to create a plan.")
        except Moderator.DoesNotExist:
            raise ValidationError("User is not a Moderator.")

        return user.role in self.roles
