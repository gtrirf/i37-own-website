from django.contrib import admin
from .models import MainInfo, Career, SocialLink


@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_add_permission(self, request):
        return not MainInfo.objects.exists()


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['app', 'url']
