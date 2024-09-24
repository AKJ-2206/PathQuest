from django.apps import AppConfig


class ElearningappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eLearningApp'

class ElearningAppConfig(AppConfig):
    name = 'eLearningApp'

    def ready(self):
        import eLearningApp.signals

class YourAppConfig(AppConfig):
    name = 'eLearningApp'

    def ready(self):
        import eLearningApp.signals
