# from django.apps import AppConfig
# import logging
# logging.warning("App initialization reached", stack_info=True)

# class ElearningappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'eLearningApp'

# class ElearningAppConfig(AppConfig):
#     name = 'eLearningApp'

#     def ready(self):
#         import eLearningApp.signals

# class YourAppConfig(AppConfig):
#     name = 'eLearningApp'

#     def ready(self):
#         import eLearningApp.signals

# class elearningAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'eLearningApp'
from django.apps import AppConfig

class ELearningAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eLearningApp'

    def ready(self):
        import eLearningApp.signals