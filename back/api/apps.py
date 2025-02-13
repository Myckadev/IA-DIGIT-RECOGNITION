from django.apps import AppConfig
from .tasks import initialize_and_save_model


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        initialize_and_save_model.delay()
