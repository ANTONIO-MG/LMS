from django.apps import AppConfig


class UsertasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usertasks'

    def ready(self):
        import usertasks.signals