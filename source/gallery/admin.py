from django.contrib import admin
from .models.photo import Photo
from .models.album import Album

admin.site.register(Photo)
admin.site.register(Album)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'author', 'created_at', 'album', 'is_private')
    list_filter = ('is_private', 'created_at', 'album')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','author', 'created_at', 'is_private')
    list_filter = ('is_private', 'created_at')

