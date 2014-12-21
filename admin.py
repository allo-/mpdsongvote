from django.contrib import admin
import models


class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ("filename", )


def playlistitem_filename(playlistvote):
    return playlistvote.playlistitem.filename
playlistitem_filename.short_description = "filename"


class PlaylistVoteAdmin(admin.ModelAdmin):
    list_display = (playlistitem_filename, "value")


class ExcludeAdmin(admin.ModelAdmin):
    list_display = ("value", "field")


class PlayedSongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "filename")


admin.site.register(models.PlaylistItem, PlaylistItemAdmin)
admin.site.register(models.PlaylistVote, PlaylistVoteAdmin)
admin.site.register(models.Exclude, ExcludeAdmin)
admin.site.register(models.PlayedSong, PlayedSongAdmin)
