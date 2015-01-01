from django.db import models


class Song(models.Model):
    filename = models.CharField(max_length=2048)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    def __unicode__(self):
        return u"Song<{0}>".format(self.filename)


class PlaylistVote(models.Model):
    song = models.ForeignKey(Song, null=True)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return "PlaylistVote<file={0}, value={1}>".format(
            self.song.filename, self.value)


class PlayedSong(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, null=True)

    def __unicode__(self):
        return "PlayedSong<{0}, {1}>".format(self.song.artist, self.song.title)


class SongFav(models.Model):
    song = models.ForeignKey(Song, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "SongFav<{0}>".format(self.song.filename)


class SongRequest(models.Model):
    date = models.DateTimeField(auto_now=True)
    song = models.ForeignKey(Song, null=True)

    def __unicode__(self):
        return "SongRequest<filename={0}>".format(self.song.filename)


class SongRequestVote(models.Model):
    songrequest = models.ForeignKey(SongRequest)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return "SongRequest<file={0}, value={1}>".format(
            self.songrequest.filename, self.value)

FIELD_TYPES = (
    ("file", "filename"),
    ("title", "title"),
    ("artist", "artist"),
)


class Exclude(models.Model):
    field = models.CharField(max_length=20, choices=FIELD_TYPES, default=0)
    value = models.CharField(max_length=2048, unique=True)
