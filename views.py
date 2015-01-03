from django.shortcuts import render, redirect, get_object_or_404
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
# remove song from the playlist, if thevotes are less or equal than this value
REMOVE_FROM_PLAYLIST_VOTES = -2


def playlist(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    update_playlist(client=c)
    playlist = c.playlistid()
    status = c.status()

    # add position in current song
    if len(playlist):
        playlist[0]['cur_time'] = status['time'].split(":")[0]

    votes = get_votes()
    favs = dict([
        (x['filename'], x['favs']) for x in Song.objects.all().annotate(
            favs=models.Count("songfav")
        ).values("filename", "favs")])
    for song in playlist:
        if song['file'] in favs:
            song['favs'] = favs[song['file']]
        else:
            song['favs'] = 0

        if song['file'] in votes:
            song['votes'] = votes[song['file']]
        else:
            song['votes'] = 0

        song['attribution'] = get_attribution(song['file'])

    current_songid = c.status()['songid']
    c.disconnect()
    return render(request, 'playlist.html', {
        'page': 'playlist',
        'current_songid': current_songid,
        'playlist': playlist,
        'status': status
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
            map(
                lambda x: unicode(
                    x.get('album', ''),
                    "utf-8",
                    errors="ignore"
                ),
                c.find("artist", artist)
            )
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
    songs = filter(
        lambda x: unicode(
            x.get('album', ''),
            "utf-8",
            errors="ignore"
        ) == album,
        c.find("artist", artist)
    )
    for song in songs:
        song['attribution'] = get_attribution(song['file'])
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
    songs = filter(
        lambda x: unicode(
            x.get('title', ''),
            "utf-8",
            errors="ignore"
        ), 
        c.find("album", album)
    )
    for song in songs:
        song['attribution'] = get_attribution(song['file'])
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

    song_obj = get_song(filename, track['artist'], track['title'])
    pv = PlaylistVote(song=song_obj, value=+1 if up else -1)
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
    song_votes = votes.get(filename, 0)
    songid = int(track['id'])
    pos = int(track['pos'])
    movepos = None

    # remove, if there are enough negative votes
    if song_votes <= REMOVE_FROM_PLAYLIST_VOTES:
        c.delete(pos)
        update_playlist(client=c)
        remove_text = "removed: {artist} - {title}"
        messages.add_message(
            request, messages.INFO, remove_text.format(
                artist=track.get("artist", "unknown artist"),
                title=track.get("title", "unknown title")
            )
        )
    elif up:
        # pos -1 .. 1 (never move before the first (playing) song)
        for plpos in xrange(pos-1, 0, -1):
            if song_votes - MIN_MOVE_DIFFERENCE \
               >= votes.get(pl[plpos]['file'], 0):
                    movepos = plpos
    else:
        # pos+1 .. end
        for plpos in xrange(pos+1, len(pl)):
            if song_votes + MIN_MOVE_DIFFERENCE \
               <= votes.get(pl[plpos]['file'], 0):
                    movepos = plpos
            else:
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
            song_obj = get_song(filename, track['artist'], track['title'])
            sr, created = SongRequest.objects.get_or_create(
                song=song_obj,
            )
            sr.save()  # safe SongRequest anyway to update timestamp
            SongRequestVote(songrequest=sr, value=+1).save()
    return redirect(request.GET.get("from", "/"))


def fav_song(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    form = FavSongForm(request.POST or None)
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
                "Faved: {artist} - {title}".format(
                    artist=track['artist'], title=track['title'])
            )
            song_obj = get_song(filename, track['artist'], track['title'])
            SongFav(song=song_obj).save()
    return redirect(request.GET.get("from", "/"))


def show_attribution(request, attribution_id):
    attribution = get_object_or_404(Attribution, id=int(attribution_id))
    return render(request, "attribution.html", {'attribution': attribution})
