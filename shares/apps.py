from django.apps import AppConfig

class SharesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shares'

    def ready(self):
        import shares.signals  # 👈 Add this
