from django.apps import AppConfig
import sys

class CovidstatsConfig(AppConfig):
    name = 'covidstats'

    def ready(self):
        if 'runserver' in sys.argv or 'CoroNow.wsgi' in sys.argv:
            from . import task
            task.main()
        return True