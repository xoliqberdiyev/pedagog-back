from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "title": _("Foydalanuvchilar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person",
                "link": reverse_lazy("admin:users_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
                "badge": lambda: __import__(
                    "apps.users.models.user"
                ).users.models.user.UserProfile.user_get_status_count(),
            },
            {
                "title": _("Guruhlar"),
                "icon": "supervisor_account",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Moderatorlar"),
                "icon": "admin_panel_settings",
                "link": reverse_lazy("admin:pedagog_moderator_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_moderator"
                ),
                "badge": lambda: __import__(
                    "apps.pedagog.models.moderator"
                ).pedagog.models.moderator.Moderator.moderator_get_status_count(),
            },
            {
                "title": _("Moderator ruxsatnomalari"),
                "icon": "admin_panel_settings",
                "link": reverse_lazy("admin:moderator_moderatorpermission_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_moderatorpermission"
                ),
                "badge": lambda: __import__(
                    "apps.moderator.models.permission"
                ).moderator.models.permission.ModeratorPermission.moderator_get_status_count(),
            },
        ],
    },
    {
        "title": _("Kalendar Tematik Reja"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Tematik reja"),
                "icon": "fact_check",
                "link": reverse_lazy("admin:pedagog_plan_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_plan"
                ),
            },
            {
                "title": _("Mavzular"),
                "icon": "checklist",
                "link": reverse_lazy("admin:pedagog_topic_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_topic"
                ),
            },
            {
                "title": _("Suniy Intellekt"),
                "icon": "network_intelligence_update",
                "link": reverse_lazy("admin:pedagog_ai_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_ai"
                ),
            },
            {
                "title": _("TMR arizalari"),
                "icon": "handshake",
                "link": reverse_lazy("admin:pedagog_tmrappeal_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_tmrappeal"
                ),
                "badge": lambda: __import__(
                    "apps.pedagog.models.tmr_appeal"
                ).pedagog.models.tmr_appeal.TMRAppeal.get_pending(),
            },
        ],
    },
    {
        "title": _("Elektron resurslar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Kategoriyalar"),
                "icon": "format_indent_increase",
                "link": reverse_lazy(
                    "admin:pedagog_electronresourcecategory_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_electronresourcecategory"
                ),
            },
            {
                "title": _("Sub Kategoriyalar"),
                "icon": "sort",
                "link": reverse_lazy(
                    "admin:pedagog_electronresourcesubcategory_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_electronresourcesubcategory"
                ),
            },
            {
                "title": _("Elektron resurslar"),
                "icon": "cloud_download",
                "link": reverse_lazy("admin:pedagog_electronresource_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_electronresource"
                ),
            },
        ],
    },
    {
        "title": _("Pedagog"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Videos"),
                "icon": "cleaning_services",
                "link": reverse_lazy("admin:pedagog_videomodel_changelist"),
            },
            {
                "title": _("Services"),
                "icon": "cleaning_services",
                "link": reverse_lazy("admin:pedagog_servicesmodel_changelist"),
            },
            {
                "title": _("Banner"),
                "icon": "planner_banner_ad_pt",
                "link": reverse_lazy("admin:pedagog_bannermodel_changelist"),
            },
            {
                "title": _("Yangiliklar"),
                "icon": "campaign",
                "link": reverse_lazy("admin:home_news_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_news"
                ),
            },
            {
                "title": _("Blog"),
                "icon": "auto_stories",
                "link": reverse_lazy("admin:home_blog_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_blog"
                ),
            },
            {
                "title": _("Privacy"),
                "icon": "security",
                "link": reverse_lazy("admin:home_privacypolicy_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_privacypolicy"
                ),
            },
            {
                "title": _("Ma'lumot"),
                "icon": "info",
                "link": reverse_lazy("admin:home_pedagoginfo_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_pedagoginfo"
                ),
            },
            {
                "title": _("Contact Us"),
                "icon": "support_agent",
                "link": reverse_lazy("admin:home_contactus_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_contactus"
                ),
            },
            {
                "title": _("Seo"),
                "icon": "web_traffic",
                "link": reverse_lazy("admin:home_seo_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_seo"
                ),
            },
        ],
    },
    {
        "title": _("Maktab turi"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Maktab turlari"),
                "icon": "school",
                "link": reverse_lazy("admin:pedagog_schooltype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_schooltype"
                ),
            },
        ],
    },
    {
        "title": _("Sinflar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Sinflar"),
                "icon": "co_present",
                "link": reverse_lazy("admin:pedagog_classes_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_classes"
                ),
            },
            {
                "title": _("Sinf guruhlari"),
                "icon": "hub",
                "link": reverse_lazy("admin:pedagog_classgroup_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_classgroup"
                ),
            },
        ],
    },
    {
        "title": _("Fanlar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Fanlar"),
                "icon": "book",
                "link": reverse_lazy("admin:pedagog_science_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_science"
                ),
            },
            {
                "title": _("Fan tillari"),
                "icon": "translate",
                "link": reverse_lazy("admin:pedagog_sciencelanguage_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_sciencelanguage"
                ),
            },
        ],
    },
    {
        "title": _("Dars jadvali"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("Choraklar"),
                "icon": "dashboard_customize",
                "link": reverse_lazy("admin:pedagog_quarter_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_quarter"
                ),
            },
            {
                "title": _("Dars jadvali"),
                "icon": "edit_calendar",
                "link": reverse_lazy("admin:pedagog_lessonschedule_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_lessonschedule"
                ),
            },
        ],
    },
    {
        "title": _("Chat"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("Chat"),
                "icon": "forum",
                "link": reverse_lazy("admin:websocket_chatroom_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_chatroom"
                ),
            },
            {
                "title": _("Xabarlar"),
                "icon": "mark_chat_read",
                "link": reverse_lazy("admin:websocket_message_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_message"
                ),
            },
        ],
    },
    {
        "title": _("Manzillar"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("Viloyatlar"),
                "icon": "location_on",
                "link": reverse_lazy("admin:users_region_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_region"
                ),
            },
            {
                "title": _("Tumanlar"),
                "icon": "my_location",
                "link": reverse_lazy("admin:users_district_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_district"
                ),
            },
        ],
    },
    {
        "title": _("Fayllar"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("Media Fayllar"),
                "icon": "share",
                "link": reverse_lazy("admin:pedagog_media_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_media"
                ),
            },
            {
                "title": _("Hujjatlar"),
                "icon": "folder_open",
                "link": reverse_lazy("admin:pedagog_document_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_document"
                ),
            },
            {
                "title": _("TMR Fayllari"),
                "icon": "drive_folder_upload",
                "link": reverse_lazy("admin:pedagog_tmrfiles_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_tmrfiles"
                ),
            },
            {
                "title": _("Yuklashlar"),
                "icon": "download",
                "link": reverse_lazy("admin:pedagog_download_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_download"
                ),
            },
        ],
    },
    {
        "title": _("To'lovlar"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("Buyurtmalar"),
                "icon": "shopping_cart",
                "link": reverse_lazy("admin:payment_orders_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_orders"
                ),
            },
            {
                "title": _("To'lovlar"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:payment_payments_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_payment"
                ),
            },
            {
                "title": _("Tariflar"),
                "icon": "shopping_bag",
                "link": reverse_lazy("admin:payment_plans_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_plans"
                ),
            },
            {
                "title": _("Transaksiyalar"),
                "icon": "receipt_long",
                "link": reverse_lazy("admin:payment_transactionmodel_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_transactionmodel"
                ),
            },
        ],
    },
    {
        "title": _("Qo'shimcha"),
        "separator": True,  # Top border
        "collapsible": True,
        "items": [
            {
                "title": _("FAQ"),
                "icon": "quiz",
                "link": reverse_lazy("admin:home_faq_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_faq"
                ),
            },
            {
                "title": _("SMS tasdiqlash"),
                "icon": "feedback",
                "link": reverse_lazy("admin:users_smsconfirm_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_smsconfirm"
                ),
            },
            {
                "title": _("Bildirishnomalar"),
                "icon": "notifications",
                "link": reverse_lazy("admin:websocket_notification_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_notification"
                ),
            },
            {
                "title": _("Darajalar"),
                "icon": "tenancy",
                "link": reverse_lazy("admin:pedagog_degree_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_degree"
                ),
            },
        ],
    },
]

TABS = [
    {
        "models": [
            "home.news",
            "home.newscategory",
        ],
        "items": [
            {
                "title": _("Yangiliklar"),
                "link": reverse_lazy("admin:home_news_changelist"),
            },
            {
                "title": _("Kategoriyalar"),
                "link": reverse_lazy("admin:home_newscategory_changelist"),
            },
        ],
    },
    {
        "models": [
            "home.blog",
            "home.blogcategory",
        ],
        "items": [
            {
                "title": _("Blog"),
                "link": reverse_lazy("admin:home_blog_changelist"),
            },
            {
                "title": _("Kategoriyalar"),
                "link": reverse_lazy("admin:home_blogcategory_changelist"),
            },
        ],
    },
]
