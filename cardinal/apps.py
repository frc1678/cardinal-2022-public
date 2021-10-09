from django.apps import AppConfig


class CardinalAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cardinal'

    def ready(self):
        # TODO - MongoDB stuff, log file opening, etc.
        print('Apps: starting cardinal')
