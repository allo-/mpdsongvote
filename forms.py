from django import forms
from mpd import MPDClient


def validate_in_playlist(filename):
    c = MPDClient()
    c.connect("localhost", 6600)
    if not len(c.playlistfind("file", filename)):
        raise forms.ValidationError(
            "Voted Track is no longer in the playlist.")
    c.disconnect()


class PlaylistVoteForm(forms.Form):
    filename = forms.CharField(
        label="Filename", max_length=2048,
        validators=[validate_in_playlist], widget=forms.HiddenInput)
