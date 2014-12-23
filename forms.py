from django import forms
from mpd import MPDClient


def validate_in_playlist(filename):
    c = MPDClient()
    c.connect("localhost", 6600)
    if not len(c.playlistfind("file", filename)):
        raise forms.ValidationError("Voted Track is no longer in the playlist.")
    c.disconnect()


def validate_exists_and_is_not_in_playlist(filename):
    c = MPDClient()
    c.connect("localhost", 6600)
    if len(c.playlistfind("file", filename)):
        raise forms.ValidationError("Song is already in the playlist.")
    elif not len(c.find("file", filename)):
        raise forms.ValidationError("Song not found.")
    c.disconnect()


def validate_exists(filename):
    c = MPDClient()
    c.connect("localhost", 6600)
    if not len(c.find("file", filename)):
        raise forms.ValidationError("Song not found.")
    c.disconnect()


class PlaylistVoteForm(forms.Form):
    filename = forms.CharField(
        label="Filename", max_length=2048,
        validators=[validate_in_playlist]
    )


class RequestSongForm(forms.Form):
    filename = forms.CharField(
        label="Filename", max_length=2048,
        validators=[validate_exists_and_is_not_in_playlist]
    )


class FavSongForm(forms.Form):
    filename = forms.CharField(
        label="Filename", max_length=2048,
        validators=[validate_exists]
    )
