from django.contrib import admin
from .models import Artist, Album, Song, Genre


# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_editable = ("name",)
    search_fields = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist")
    list_editable = ("title", "artist")
    search_fields = ("title",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "album")
    list_editable = ("title", "artist", "album")
    search_fields = ("title",)

class ObjectInline(admin.TabularInline):
    model = Song
    fields = ('title', 'artist', 'album', 'genre', 'audio_file')
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_editable = ("name",)
    list_display = ("id", "name")


