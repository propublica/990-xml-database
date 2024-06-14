import os

from django.apps import AppConfig


class MetadataConfig(AppConfig):
    name = "irsdb.schemas"
    verbose_name = "IRSdb - Schemas"
    path = os.path.dirname(__file__)
