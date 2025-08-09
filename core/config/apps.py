THIRD_PARTY_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",

    # payment
    "click_up",
    "payme",

    "modeltranslation",
    "django_ckeditor_5",
    "corsheaders",
    "rosetta",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "import_export",
]

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

PROJECT_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.shared.apps.SharedConfig",
    "apps.home.apps.HomeConfig",
    "apps.payment.apps.PaymentConfig",
    "apps.pedagog.apps.PedagogConfig",
    "apps.websocket.apps.WebsocketConfig",
    "apps.moderator.apps.ModeratorConfig",
]
