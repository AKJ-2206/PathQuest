from django.apps import AppConfig
import logging

class ELearningAppConfig(AppConfig):
    name = 'eLearningApp'

    def ready(self):
        # Place any initialization logic here, like logging
        logging.warning("App initialization reached", stack_info=True)
