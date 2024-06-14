from django.apps import AppConfig
import os


class BaseConfig(AppConfig):
    name = "irsdb.return"
    verbose_name = "IRSdb - Return"
    path = os.path.dirname(__file__)
