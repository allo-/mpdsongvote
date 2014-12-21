from django.contrib import admin
import models


def playlistitem_filename(playlistvote):
    return playlistvote.playlistitem.filename
playlistitem_filename.short_description = "filename"


def songrequest_filename(songrequestvote):
    return songrequestvote.songrequest.filename
songrequest_filename.short_description = "filename"


class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ("filename", )


class PlaylistVoteAdmin(admin.ModelAdmin):
    list_display = (playlistitem_filename, "value")


class SongRequestAdmin(admin.ModelAdmin):
    list_display = ("filename", )


class SongRequestVoteAdmin(admin.ModelAdmin):
    list_display = (songrequest_filename, "value")


class ExcludeAdmin(admin.ModelAdmin):
    list_display = ("value", "field")


class PlayedSongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "filename")


admin.site.register(models.PlaylistItem, PlaylistItemAdmin)
admin.site.register(models.PlaylistVote, PlaylistVoteAdmin)

admin.site.register(models.SongRequest, SongRequestAdmin)
admin.site.register(models.SongRequestVote, SongRequestVoteAdmin)

admin.site.register(models.Exclude, ExcludeAdmin)
admin.site.register(models.PlayedSong, PlayedSongAdmin)
