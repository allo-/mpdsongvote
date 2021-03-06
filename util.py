from mpd import MPDClient
from models import *


def get_track(filename, in_playlist=True, client=None):
    if not client:
        c = MPDClient()
        c.connect("localhost", 6600)
    else:
        c = client

    if in_playlist:
        track = c.playlistfind('file', filename)
    else:
        track = c.find('file', filename)
    track = track[0] if track else None
    if track and 'artist' not in track:
        track['artist'] = ""
    if track and 'title' not in track:
        track['title'] = title_from_filename(track['file'])
    return track


def get_votes():
    songs = Song.objects.all().annotate(
        votes=models.Sum('playlistvote__value')).exclude(votes=None)
    return dict([(x.filename, x.votes) for x in songs])


def to_unicode(string):
    if not isinstance(string, unicode):
        string = unicode(string, "utf-8", errors="ignore")
    return string


def get_attribution(filename):
    filename = to_unicode(filename)
    songs = Song.objects.filter(filename=filename)
    song = songs[0] if songs else None
    if song:
        if song.attribution:
            return song.attribution

    attributions = Attribution.objects.all().extra(
        select={'length': 'LENGTH(filename)'}
    ).order_by('-length')
    for attribution in attributions:
        if filename.startswith(attribution.filename):
            if song:
                song.attribution = attribution
                song.save()
            return attribution
    return None


def get_song(filename, artist, title):
    song_obj, created = Song.objects.get_or_create(filename=filename)
    if created:
        song_obj.artist = artist
        song_obj.title = title
        song_obj.attribution = get_attribution(filename)
        song_obj.save()
    return song_obj


def add_num_requests_to_songlist(songlist):
    """
        add the number of requests to a list of dicts, containing
        a 'file' ore 'filename' key to the key 'votes'
    """
    # list of all SongRequests with votes count
    vote_counts = SongRequest.objects.all().annotate(
        votes=models.Sum("songrequestvote__value"))
    # map filename to votes
    vote_counts = dict([(x.song.filename, x.votes) for x in vote_counts])

    for song in songlist:
        song['votes'] = 0
        # if its a song, the filename is stored in 'file'
        filename = None
        if 'filename' not in song:
            if 'file' in song:
                filename = song['file']
            elif 'song__filename' in song:
                filename = song['song__filename']
            else:
                continue

        # add the votes, if there are any
        if filename in vote_counts:
            song['votes'] = vote_counts[filename]

    return songlist


def title_from_filename(value):
    # remove path
    filename = value.split("/")[-1]
    # remove file extension
    parts = filename.split(".")
    if len(parts) == 1:
        return parts[0]
    else:
        return ".".join(parts[:-1])
