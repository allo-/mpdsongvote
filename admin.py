from django.contrib import admin
import django.db.models
import models


def song_filename(instance):
    return instance.song.filename
song_filename.short_description = "filename"


def song_artist(instance):
    return instance.song.filename
song_artist.short_description = "artist"


def song_title(instance):
    return instance.song.title
song_title.short_description = "title"


def songrequest_votes(songrequest):
    return models.SongRequestVote.objects.filter(
        songrequest=songrequest).aggregate(
        votes=django.db.models.Sum("value"))['votes']
songrequest_votes.short_description = "votes"


class PlaylistVoteAdmin(admin.ModelAdmin):
    list_display = (song_filename, "value")


class SongRequestAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)
    list_display = (song_filename, songrequest_votes, "date")


class SongRequestVoteAdmin(admin.ModelAdmin):
    list_display = (song_filename, "value")


class ExcludeAdmin(admin.ModelAdmin):
    list_display = ("value", "field")


class PlayedSongAdmin(admin.ModelAdmin):
    list_display = (song_title, song_artist, song_filename, "date")


class SongAdmin(admin.ModelAdmin):
    list_display = ("filename",)


class SongFavAdmin(admin.ModelAdmin):
    list_display = (song_filename, "date")


admin.site.register(models.PlaylistVote, PlaylistVoteAdmin)

admin.site.register(models.Song, SongAdmin)
admin.site.register(models.SongFav, SongFavAdmin)

admin.site.register(models.SongRequest, SongRequestAdmin)
admin.site.register(models.SongRequestVote, SongRequestVoteAdmin)

admin.site.register(models.Exclude, ExcludeAdmin)
admin.site.register(models.PlayedSong, PlayedSongAdmin)
