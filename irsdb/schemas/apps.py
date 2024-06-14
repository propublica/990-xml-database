from django.apps import AppConfig
import os


class MetadataConfig(AppConfig):
    name = "irsdb.schemas"
    verbose_name = "IRSdb - Schemas"
    path = os.path.dirname(__file__)
