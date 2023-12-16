from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self) -> None:
        from .management.scheduler import start_task
        start_task()
        return super().ready()
