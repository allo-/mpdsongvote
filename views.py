from django.shortcuts import render
from mpd import MPDClient

def playlist(request):
    c = MPDClient()
    c.connect("localhost", 6600)
    playlist = c.playlistid()
    c.disconnect()
    return render(request, 'playlist.html', {
        'page': 'playlist',
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
    albums = filter(lambda x: x, set(map(lambda x: x.get('album', None), c.find("artist", artist))))
    c.disconnect()
    return render(request, 'artist.html', {
        'page': 'artist_albums',
        'artist': artist,
        'albums': albums
    })

def artist_album_songs(request, artist, album):
    c = MPDClient()
    c.connect("localhost", 6600)
    songs = filter(lambda x: x.get('album', None) == album, c.find("artist", artist))
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
