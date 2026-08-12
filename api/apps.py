from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        """Runs once when Django starts."""
        # Optional: Import signals here to avoid circular dependencies
        # import api.signals
