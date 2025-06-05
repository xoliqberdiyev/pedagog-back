from django.urls import path

from apps.pedagog.views.admin_site import (
    ModeratorAdminSiteView,
    ModeratorAdminSiteDetailView,
)
from apps.pedagog.views.ai import AiAPIView
from apps.pedagog.views.change_role import ChangeRoleView
from apps.pedagog.views.classes import ClassesListView, ClassGroupListView
from apps.pedagog.views.degree import DegreeListView
from apps.pedagog.views.download import (
    DownloadMediaView,
    DownloadFileView,
    MobileDownloadHistoryView,
    MobileUploadHistoryView,
)
from apps.pedagog.views.electron_resource import (
    ElectronResourceCategoryView,
    ElectronResourceCategoryDetailView,
    ElectronResourceSubCategoryView,
    ElectronResourceSubCategoryDetailView,
    ElectronResourceView,
    ElectronResourceDetailView,
    ElectronResourceAdminView,
)
from apps.pedagog.views.media import MediaApiView, MediaDetailApiView
from apps.pedagog.views.moderator import (
    ModeratorCreateViewSet,
    ModeratorListView,
    ModeratorDetailView,
    SendMoneyToModerators,
    ModeratorElectronResourcesApiView,
    ModeratorTemetikPlanApiView,
)
from apps.pedagog.views.plan import PlanApiView, PlanAdminListAPIView, PlanDetailView
from apps.pedagog.views.quarter import QuarterListView, ModeratorQuarterApiView
from apps.pedagog.views.school import SchoolTypeListView
from apps.pedagog.views.science import ScienceListView, ScienceLanguageListView
from apps.pedagog.views.tmr_appeal import TMRAppealAPIView, TmrFilesAPIView
from apps.pedagog.views.topic import TopicApiView, TopicDetailApiView

urlpatterns = [
    path(
        "download/get/<int:media_id>/",
        DownloadMediaView.as_view(),
        name="download_resource",
    ),
    path(
        "download/set/<uuid:download_token>/",
        DownloadFileView.as_view(),
        name="download_file",
    ),
    path(
        "tmr_appeal/",
        TMRAppealAPIView.as_view(),
        name="moderator-resource",
    ),
    path(
        "tmr_files/",
        TmrFilesAPIView.as_view(),
        name="moderator-resource",
    ),
    path("quarters/", QuarterListView.as_view(), name="quarter-list"),
    path("degree/", DegreeListView.as_view(), name="degree-list"),
    path(
        "change-role/",
        ChangeRoleView.as_view(),
        name="change-user-role",
    ),
    path("moderator/", ModeratorCreateViewSet.as_view(), name="moderator"),
    path("moderator/list/", ModeratorListView.as_view(), name="moderator-list"),
    path(
        "moderator/detail/<int:pk>/",
        ModeratorDetailView.as_view(),
        name="moderator-detail",
    ),
    path("send/money/", SendMoneyToModerators.as_view(), name="send-money"),
    path(
        "moderator/electron/resource/<int:moderator_id>/",
        ModeratorElectronResourcesApiView.as_view(),
        name="moderator-electron-resource-list",
    ),
    path(
        "ai/",
        AiAPIView.as_view(),
        name="ai",
    ),
    path("plan/", PlanApiView.as_view(), name="plan"),
    path("plan/<int:pk>/", PlanDetailView.as_view(), name="plan"),
    path("topic/", TopicApiView.as_view(), name="topic"),
    path("topic/<int:pk>/", TopicDetailApiView.as_view(), name="topic-detail"),
    path("media/", MediaApiView.as_view(), name="media"),
    path("media/<int:pk>/", MediaDetailApiView.as_view(), name="media"),
    path("school/type/", SchoolTypeListView.as_view(), name="school-type"),
    path("classes/", ClassesListView.as_view(), name="classes"),
    path("classes/group/", ClassGroupListView.as_view(), name="classes-group"),
    path("science/", ScienceListView.as_view(), name="science"),
    path(
        "science/language/", ScienceLanguageListView.as_view(), name="science-language"
    ),
    path(
        "history/download/",
        MobileDownloadHistoryView.as_view(),
        name="download_history",
    ),
    path(
        "history/upload/",
        MobileUploadHistoryView.as_view(),
        name="upload_history",
    ),
    ############################################################################################################
    # Permission bor bo'lgan foydalanuvchilar uchun
    ############################################################################################################
    path(
        "moderator/plan/<int:moderator_id>/",
        ModeratorTemetikPlanApiView.as_view(),
        name="moderator-plan-list",
    ),
    path(
        "moderator/quarters/",
        ModeratorQuarterApiView.as_view(),
        name="moderator-quarters",
    ),
    path(
        "electron-resource/category/",
        ElectronResourceCategoryView.as_view(),
        name="electron-resource-category",
    ),
    path(
        "electron-resource/category/<int:pk>/",
        ElectronResourceCategoryDetailView.as_view(),
        name="electron-resource-category-detail",
    ),
    path(
        "electron-resource/sub-category/",
        ElectronResourceSubCategoryView.as_view(),
        name="electron-resource-sub-category",
    ),
    path(
        "electron-resource/sub-category/<int:pk>/",
        ElectronResourceSubCategoryDetailView.as_view(),
        name="electron-resource-sub-category-detail",
    ),
    path(
        "electron-resource/files/",
        ElectronResourceView.as_view(),
        name="electron-resource-files",
    ),
    path(
        "electron-resource/files/<int:pk>/",
        ElectronResourceDetailView.as_view(),
        name="electron-resource-files-detail",
    ),
    path("admin-site/moderator/", ModeratorAdminSiteView.as_view()),
    path(
        "admin-site/moderator/<int:pk>/",
        ModeratorAdminSiteDetailView.as_view(),
    ),
    path("plan/admin/", PlanAdminListAPIView.as_view(), name="plan-admin"),
    path(
        "electron-resource/admin/",
        ElectronResourceAdminView.as_view(),
        name="electron-resources-admin",
    ),
]
