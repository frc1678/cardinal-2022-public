from django.apps import AppConfig
import pymongo

from .api import cardinal_data_request as cdr

# See ldc, database, clouddb from 'server'.
class CardinalAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cardinal'

    def ready(self):
        cdr.CLIENT = pymongo.MongoClient(cdr.CONNECTION_STR, cdr.PORT)
        cdr.DB = cdr.CLIENT['2020caln']
