from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mpd import MPDClient
from urllib import quote, unquote
from django.db import models
from models import *


def playlist(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    playlist = c.playlistid()

    playlistitems = PlaylistItem.objects.all().annotate(
        votes=models.Sum('playlistvote__value')).values()
    votes = dict([(x['filename'], x['votes']) for x in playlistitems])

    for song in playlist:
        if song['file'] in votes:
            song['votes'] = votes[song['file']]
        else:
            song['votes'] = 0
        song['quoted_filename'] = quote(song['file']).replace("/", "%2F")
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
    filename = unquote(quoted_filename)
    pi, pi_created = PlaylistItem.objects.get_or_create(filename=filename)
    if pi_created:
        pi.save()
    pv = PlaylistVote(playlistitem=pi, value=+1 if up else -1)
    pv.save()
    return redirect(reverse(playlist))
