from django.apps import AppConfig


class NishatiflexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nishatiflex'

    def ready(self):
        import nishatiflex.signals
