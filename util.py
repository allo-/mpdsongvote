from mpd import MPDClient
from models import *


def get_track(filename, in_playlist=True, client=None):
    if not client:
        c = MPDClient()
        c.connect("localhost", 6600)
    else:
        c = client

    if in_playlist:
        track = c.playlistfind("file", filename)
    else:
        track = c.find("file", filename)
    track = track[0] if track else None
    return track


def get_votes():
    playlistitems = PlaylistItem.objects.all().annotate(
        votes=models.Sum('playlistvote__value')).values()
    return dict([(x['filename'], x['votes']) for x in playlistitems])


def add_num_requests_to_songlist(songlist):
    # list of all SongRequests with votes count
    vote_counts = SongRequest.objects.all().annotate(
        votes=models.Sum("songrequestvote__value")).values("filename", "votes")
    # map filename to votes
    vote_counts = dict([(x['filename'], x['votes']) for x in vote_counts])

    for song in songlist:
        song['votes'] = 0
        # if its a playlistitem, the filename is stored in 'file'
        if not 'filename' in song:
            if 'file' in song:
                song['filename'] = song['file']
            else:
                continue

        # add the votes, if there are any
        if song['filename'] in vote_counts:
            song['votes'] = vote_counts[song['filename']]

    return songlist
