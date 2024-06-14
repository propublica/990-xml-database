import os

from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "irsdb.filing"
    verbose_name = "IRSdb - Filing"
    path = os.path.dirname(__file__)
