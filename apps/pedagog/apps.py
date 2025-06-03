from django.apps import AppConfig


class PedagogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pedagog"

    def ready(self):
        import apps.pedagog.signals  # noqa
