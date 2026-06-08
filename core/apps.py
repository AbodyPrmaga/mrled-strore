from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    name = 'core'
    
    def ready(self):
        if os.getenv("CREATE_SUPERUSER") == "1":
            from .create_admin import create_superuser
            create_superuser()
