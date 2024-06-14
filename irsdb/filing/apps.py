from django.apps import AppConfig
import os


class BaseConfig(AppConfig):
    name = "irsdb.filing"
    verbose_name = "IRSdb - Filing"
    path = os.path.dirname(__file__)
