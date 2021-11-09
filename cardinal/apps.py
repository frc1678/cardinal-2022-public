from django.apps import AppConfig
import pymongo
from datetime import datetime
import subprocess

from .api import cardinal_data_request as cdr
from .api.logger import log, Severity

# See ldc, database, clouddb from 'server'.
class CardinalAPIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cardinal"

    commit = (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    )

    log(f"Started Cardinal at {datetime.now()}", Severity.DEBUG)
    log(f"Started with commit {commit}", Severity.DEBUG)

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
