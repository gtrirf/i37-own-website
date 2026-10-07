from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'

    def ready(self):
        from apps.images import register_webp_fields
        from .models import ProjectImage
        register_webp_fields(ProjectImage, 'photo')
