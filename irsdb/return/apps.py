import os

from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "irsdb.return"
    verbose_name = "IRSdb - Return"
    path = os.path.dirname(__file__)
