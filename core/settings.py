import os  # noqa
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv, find_dotenv

from core.config import *  # noqa

load_dotenv(find_dotenv(".env"))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = os.getenv("DEBUG")
if DEBUG is not None:
    DEBUG = DEBUG.lower() in ["true", "1"]
else:
    DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

INSTALLED_APPS = [*THIRD_PARTY_APPS, *DEFAULT_APPS, *PROJECT_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "assets/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "uz"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("ru", _("Russia")),
    ("en", _("English")),
    ("uz", _("Uzbek")),
    ("ko", _("Kirill")),
)

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en", "ko")

MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"

STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("assets/static"))]
STATIC_ROOT = str(BASE_DIR.joinpath("assets/staticfiles"))

MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("assets/media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "source",
    "Referral-Code",
    'web_session',
]
CORS_ALLOW_ALL_HEADERS = True

    

CORS_ALLOW_ALL_ORIGINS = True

LOCALE_MIDDLEWARE_EXCLUDED_PATHS = ["/media/", "/static/"]

DATA_UPLOAD_MAX_MEMORY_SIZE = 734003200  # 700 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 734003200  # 700 MB

MEDIA_AMOUNT = 6000


# click
# CLICK_SERVICE_ID=os.getenv("CLICK_SERVICE_ID")
# CLICK_MERCHANT_ID=os.getenv("CLICK_MERCHANT_ID")
# CLICK_SECRET_KEY=os.getenv("CLICK_SECRET_KEY")
# CLICK_TOKEN = os.getenv("CLICK_TOKEN")
CLICK_ACCOUNT_MODEL = "apps.payment.models.models.Orders" 
CLICK_AMOUNT_FIELD = "price" 
# CLICK_SERVICE_2_ID=os.getenv('CLICK_SERVICE_2_ID')
# CLICK_MERCHANT_2_ID=os.getenv('CLICK_MERCHANT_2_ID')

#payme
PAYME_ID=os.getenv("PAYME_ID")
PAYME_KEY=os.getenv("PAYME_KEY")
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "price"
PAYME_ACCOUNT_MODEL = "apps.payment.models.models.Orders"
PAYME_ONE_TIME_PAYMENT = True