from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self):
        from apps.images import register_webp_fields
        from .models import MainInfo, Career
        register_webp_fields(MainInfo, 'photo')
        register_webp_fields(Career, 'logo')
