from django.contrib import admin
from .models import Project, ProjectImage, ProjectTechnology


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['photo', 'alt_txt', 'caption', 'sort_order']


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1
    fields = ['name', 'color']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline, ProjectTechnologyInline]
    list_display = ['title', 'view_counts', 'url_link', 'created_at']
    search_fields = ['title']
    readonly_fields = ['view_counts', 'created_at', 'updated_at']
