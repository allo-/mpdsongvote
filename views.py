from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mpd import MPDClient
from django.db import models
from django.contrib import messages
from models import *
from forms import *
from util import *
from update_playlist import update_playlist


# minimum vote difference for a song to be moved up/down
MIN_MOVE_DIFFERENCE = 1


def playlist(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    update_playlist(client=c)
    playlist = c.playlistid()

    votes = get_votes()

    for song in playlist:
        if song['file'] in votes:
            song['votes'] = votes[song['file']]
        else:
            song['votes'] = 0
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
    add_num_requests_to_songlist(songs)
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
    add_num_requests_to_songlist(songs)
    c.disconnect()
    return render(request, 'songs.html', {
        'page': 'album_songs',
        'album': album,
        'songs': songs
    })

def playlist_vote(request, up):
    c = MPDClient()
    c.connect("localhost", 6600)
    update_playlist(client=c)

    form = PlaylistVoteForm(request.POST or None)
    if not form.is_valid():
        for error in form.errors:
            messages.add_message(
                request, messages.ERROR,
                "{0}".format(form.errors[error][0])
            )
        return redirect(reverse(playlist))
    filename = form.cleaned_data['filename']

    pl = c.playlistid()
    track = get_track(filename, in_playlist=True, client=c)

    # track not in playlist
    if not track:
        return redirect(reverse(playlist))

    pi, pi_created = PlaylistItem.objects.get_or_create(filename=filename)
    if pi_created:
        pi.save()
    pv = PlaylistVote(playlistitem=pi, value=+1 if up else -1)
    pv.save()

    if up:
        voted_text = "Voted up: {artist} - {title}"
    else:
        voted_text = "Voted down: {artist} - {title}"

    messages.add_message(
        request, messages.INFO, voted_text.format(
            artist=track.get("artist", "unknown artist"),
            title=track.get("title", "unknown title")
        )
    )

    votes = get_votes()
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
                    break

    if movepos is not None:
        c.moveid(songid, movepos)
        if up:
            voted_text = "Moved up: {artist} - {title}"
        else:
            voted_text = "Moved down: {artist} - {title}"
        messages.add_message(
            request, messages.INFO, voted_text.format(
                artist=track.get("artist", "unknown artist"),
                title=track.get("title", "unknown title")
            )
        )

    c.disconnect()
    return redirect(reverse(playlist))

def request_song(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    form = RequestSongForm(request.POST or None)
    if not form.is_valid():
        for error in form.errors:
            messages.add_message(
                request,
                messages.ERROR,
                "Error: {0}".format(form.errors[error][0])
            )
    else:
        filename = form.cleaned_data['filename']
        track = get_track(filename, in_playlist=False)
        if not track:
            messages.add_message(
                request,
                messages.ERROR,
                "Error: Cannot find song."
            )
        else:
            messages.add_message(
                request,
                messages.INFO,
                "Requested: {artist} - {title}".format(
                    artist=track['artist'], title=track['title'])
            )
            sr, created = SongRequest.objects.get_or_create(filename=filename)
            if created:
                sr.artist = track.get('artist', 'unknown artist')
                sr.title = track.get('title', 'unknown title')
            sr.save()  # safe SongRequest anyway to update timestamp
            SongRequestVote(songrequest=sr, value=+1).save()
    return redirect(request.GET.get("from", "/"))
