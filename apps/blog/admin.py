from django.contrib import admin
from .models import BlogType, Blog, BlogImage


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ['photo', 'alt_txt', 'caption', 'sort_order']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    list_display = ['title', 'blog_type', 'view_counts', 'created_at']
    list_filter = ['blog_type']
    search_fields = ['title']
    readonly_fields = ['view_counts', 'created_at', 'updated_at']
