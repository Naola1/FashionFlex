from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        import user.api.signals  # Imports the signals to make sure they're active when the app loads