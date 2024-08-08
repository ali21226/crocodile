# Crawl/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Photo, Audio, Email


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'size', 'url', 'image_tag')
    readonly_fields = ('id', 'website_name', 'size', 'image_tag')
    fields = ('url', 'size', 'path', 'id', 'website_name', 'image', 'avatar', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"

    image_tag.short_description = 'Preview'


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'size', 'url')
    readonly_fields = ('id', 'website_name', 'size')
    fields = ('url', 'size', 'path', 'id', 'website_name', 'audio')


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'email', 'url')
    readonly_fields = ('id', 'website_name')
    fields = ('email', 'url', 'path', 'id', 'website_name')
