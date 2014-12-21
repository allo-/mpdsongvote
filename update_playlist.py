#!/usr/bin/env python
import random
import mpd
from mpdsongvote import models


PLAYLIST_LENGTH = 100  # desired playlist length after removing/adding songs


def main_print(main, args):
    if main:
        print args


def update_playlist(main=False, client=None):
    if client:
        c = client
    else:
        c = mpd.MPDClient()
        c.connect("localhost", 6600)

    # 1) remove played songs from the beginning
    playlist_songs_by_pos = dict(map(
        lambda x: (int(x['pos']), x),
        c.playlistid()
    ))
    current_song_no = int(c.status()['song'])

    main_print(main, "")
    main_print(main, "removing:")
    for i in xrange(current_song_no):
        filename = playlist_songs_by_pos[i]['file']
        title = playlist_songs_by_pos[i]['title']
        artist = playlist_songs_by_pos[i]['artist']
        models.PlayedSong(
            title=title, artist=artist, filename=filename).save()
        main_print(main, filename)
        c.delete(0)
        models.PlaylistItem.objects.filter(filename=filename).delete()

    # 2) add new songs at the bottom
    playlist_songs = dict(map(lambda x: (x['file'], x), c.playlistid()))
    all_songs = dict(map(lambda x: (x['file'], x), c.search("file", "")))

    new_files = list(set(all_songs).difference(playlist_songs))

    # copy, so we can modify new_files in the exclude loop
    new_files2 = [nf for nf in new_files]
    # filter files from exclude criteria
    for exclude in models.Exclude.objects.all():
        for nf in new_files2:
            if exclude.value in all_songs[nf][exclude.field]:
                new_files.remove(nf)

    # limit playlist size
    new_files = new_files[0:max(0, PLAYLIST_LENGTH - len(playlist_songs))]
    random.shuffle(new_files)

    main_print(main, "adding:")
    for thefile in new_files:
        main_print(main, thefile)
        c.add(thefile)

    if not client:
        c.disconnect()

if __name__ == "__main__":
    import django
    django.setup()
    update_playlist(main=True)
