from django.db import models


class PlaylistItem(models.Model):
    filename = models.CharField(max_length=2048, unique=True)

    def __unicode__(self):
        return "PlaylistItem<filename={0}>".format(self.filename)


class PlaylistVote(models.Model):
    playlistitem = models.ForeignKey(PlaylistItem)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return "PlaylistVote<file={0}, up={1}>".format(
            self.playlistitem.filename, self.up)
