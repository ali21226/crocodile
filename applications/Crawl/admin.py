from django.contrib import admin
from django.utils.html import format_html
from .models import Photo, Audio, Email

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'size', 'url', 'insert_time' , 'image_tag' )
    list_filter = ('website_name', 'insert_time')
    search_fields = ('website_name',)
    readonly_fields = ('id', 'website_name', 'size', 'image_tag', 'insert_time')
    fields = ('url', 'size', 'path', 'id', 'website_name', 'image', 'avatar', 'image_tag', 'insert_time')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"

    image_tag.short_description = 'Preview'

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'size', 'url', 'insert_time')
    list_filter = ('website_name', 'insert_time')
    readonly_fields = ('id', 'website_name', 'size', 'insert_time')
    fields = ('url', 'size', 'path', 'id', 'website_name', 'audio', 'insert_time')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'website_name', 'email', 'url', 'insert_time')
    list_filter = ('website_name', 'insert_time')
    search_fields = ('email',)
    readonly_fields = ('id', 'website_name', 'insert_time')
    fields = ('email', 'url', 'path', 'id', 'website_name', 'insert_time')
