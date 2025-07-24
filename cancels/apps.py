from django.apps import AppConfig


class CancelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cancels'

    def ready(self):
        import shares.signals

