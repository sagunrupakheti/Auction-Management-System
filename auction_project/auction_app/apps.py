from django.apps import AppConfig
import os

class AuctionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction_app'

    def ready(self):
        from . import bgTask

        if os.environ.get('RUN_MAIN', None) != 'true':
            bgTask.start_scheduler()
