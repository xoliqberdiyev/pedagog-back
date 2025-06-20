"""
Accounts app urls
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from apps.users.views.change_password import ChangePasswordView
from apps.users.views.delete_account import DeleteAccountView
from apps.users.views.document import DocumentView, DocumentDetailView
from apps.users.views.locations import RegionAPIView, DistrictAPIView
from apps.users.views.moderator import ModeratorRegisterView
from apps.users.views.profile import UserProfileView, UserProfileDetailView
from apps.users.views.sms import (
    ConfirmView,
    RegisterView,
    ResendView,
    MeView,
    MeUpdateView,
    CustomTokenObtainPairView,
    ResetPasswordView,
    ResetConfirmationCodeView,
    ResetSetPasswordView,
)

urlpatterns = [
    path("auth/confirm/", ConfirmView.as_view(), name="confirm"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path(
        "auth/register/moderator/",
        ModeratorRegisterView.as_view(),
        name="register-moderator",
    ),
    path("auth/resend/", ResendView.as_view(), name="resend"),
    path("auth/me/", MeView.as_view({"get": "get"}), name="me"),
    path("auth/me/update/", MeUpdateView.as_view(), name="me-update"),
    path(
        "auth/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "auth/reset/password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "auth/reset/confirm/",
        ResetConfirmationCodeView.as_view(),
        name="reset-confirmation-code",
    ),
    path(
        "auth/reset/set/",
        ResetSetPasswordView.as_view(),
        name="set-password",
    ),
    path(
        "auth/change/password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "auth/delete/account/",
        DeleteAccountView.as_view(),
        name="delete-account",
    ),
    path("region/", RegionAPIView.as_view(), name="region"),
    path("district/", DistrictAPIView.as_view(), name="district"),
    path("user/profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "user/profile/<int:pk>/",
        UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path("user/document/", DocumentView.as_view(), name="user-profile-document"),
    path(
        "user/document/<int:pk>/",
        DocumentDetailView.as_view(),
        name="user-profile-document-detail",
    ),
]
