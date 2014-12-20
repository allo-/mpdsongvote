from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mpd import MPDClient
from urllib import quote_plus, unquote_plus
from django.db import models
from models import *


# minimum vote difference for a song to be moved up/down
MIN_MOVE_DIFFERENCE = 2


def _get_votes():
    playlistitems = PlaylistItem.objects.all().annotate(
        votes=models.Sum('playlistvote__value')).values()
    return dict([(x['filename'], x['votes']) for x in playlistitems])


def playlist(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    playlist = c.playlistid()

    votes = _get_votes()

    for song in playlist:
        if song['file'] in votes:
            song['votes'] = votes[song['file']]
        else:
            song['votes'] = 0
        song['quoted_filename'] = quote_plus(song['file']).replace("/", "%2F")
    current_songid = c.status()['songid']
    c.disconnect()
    return render(request, 'playlist.html', {
        'page': 'playlist',
        'current_songid': current_songid,
        'playlist': playlist
    })


def artists(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    artists = filter(lambda x: x, c.list("artist"))
    c.disconnect()
    return render(request, 'artists.html', {
        'page': 'playlist',
        'artists': artists,
    })


def albums(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    albums = filter(lambda x: x, c.list("album"))
    c.disconnect()
    return render(request, 'albums.html', {
        'page': 'playlist',
        'albums': albums,
    })


def artist_albums(request, artist):
    c = MPDClient()
    c.connect("localhost", 6600)
    albums = filter(
        lambda x: x,
        set(
            map(lambda x: x.get('album', None), c.find("artist", artist))
        )
    )
    c.disconnect()
    return render(request, 'artist.html', {
        'page': 'artist_albums',
        'artist': artist,
        'albums': albums
    })


def artist_album_songs(request, artist, album):
    c = MPDClient()
    c.connect("localhost", 6600)
    songs = filter(lambda x: x.get('album', None) == album,
                   c.find("artist", artist))
    c.disconnect()
    return render(request, 'songs.html', {
        'page': 'artist_album_songs',
        'artist': artist,
        'album': album,
        'songs': songs
    })


def album_songs(request, album):
    c = MPDClient()
    c.connect("localhost", 6600)
    songs = filter(lambda x: x.get('title', None), c.find("album", album))
    c.disconnect()
    return render(request, 'songs.html', {
        'page': 'album_songs',
        'album': album,
        'songs': songs
    })


def playlist_vote(request, quoted_filename, up):
    c = MPDClient()
    c.connect("localhost", 6600)
    filename = unquote_plus(quoted_filename)
    pi, pi_created = PlaylistItem.objects.get_or_create(filename=filename)
    if pi_created:
        pi.save()
    pv = PlaylistVote(playlistitem=pi, value=+1 if up else -1)
    pv.save()

    pl = c.playlistid()
    tracks = filter(lambda x: x['file'] == filename, pl)
    # track not in playlist
    if not len(tracks):
        return redirect(reverse(playlist))
    elif len(tracks) > 1:
        # TODO: remove all but the first one from playlist
        pass
    votes = _get_votes()

    track = tracks[0]
    songid = int(track['id'])
    pos = int(track['pos'])
    movepos = None
    if up:
        # pos -1 .. 1 (never move before the first (playing) song)
        for plpos in xrange(pos-1, 0, -1):
            if votes.get(filename, 0) - MIN_MOVE_DIFFERENCE \
               >= votes.get(pl[plpos]['file'], 0):
                    movepos = plpos
    else:
        # pos+1 .. end
        for plpos in xrange(pos+1, len(pl)):
            if votes.get(filename, 0) + MIN_MOVE_DIFFERENCE \
               <= votes.get(pl[plpos]['file'], 0):
                    movepos = plpos

    if movepos is not None:
        c.moveid(songid, movepos)

    c.disconnect()
    return redirect(reverse(playlist))
