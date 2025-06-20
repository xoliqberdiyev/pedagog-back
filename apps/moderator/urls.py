from django.urls import path

from apps.moderator.views.permission import ModeratorPermissionView

urlpatterns = [
    path(
        "moderator/permissions/",
        ModeratorPermissionView.as_view(),
        name="moderator-permissions",
    ),
]
