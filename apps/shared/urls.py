from django.urls import path

from apps.shared.views.base import HomeView

# from apps.shared.views.dashboard import DashboardView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("admin/dashboard/", DashboardView.as_view(), name="dashboard"),
]
