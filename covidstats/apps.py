from django.apps import AppConfig
import sys

class CovidstatsConfig(AppConfig):
    name = 'covidstats'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from . import task
        task.main()