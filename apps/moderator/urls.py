from django.urls import path

from apps.moderator.views.permission import ModeratorPermissionView

urlpatterns = [
    path(
        "permissions/", ModeratorPermissionView.as_view(), name="moderator-permissions"
    ),
]
