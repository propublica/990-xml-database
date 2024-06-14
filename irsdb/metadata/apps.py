import os

from django.apps import AppConfig


class MetadataConfig(AppConfig):
    name = "irsdb.metadata"
    verbose_name = "IRSdb - Metadata"
    path = os.path.dirname(__file__)
