from django.apps import AppConfig
import pymongo

from .api import cardinal_data_request as cdr

# See ldc, database, clouddb from 'server'.
class CardinalAPIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cardinal"

    def ready(self):

        # Get the password string and whatnot
        try:
            with open("password.txt", "r") as file:
                password = file.read().rstrip("\n")
        except FileNotFoundError:
            print("You need to have a file named password.txt with the cloud password.")
            exit(1)

        cdr.CLIENT = pymongo.MongoClient(cdr.CONNECTION_STR.format(password), cdr.PORT)
        cdr.DB = cdr.CLIENT["2021cc"]
