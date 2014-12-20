#!/usr/bin/env python
import random
import mpd
import mpdsongvote.models


PLAYLIST_LENGTH = 100  # desired playlist length after removing/adding songs


def main_print(main, args):
    if main:
        print args


def update_playlist(main=False):
    c = mpd.MPDClient()
    c.connect("localhost", 6600)

    # 1) remove played songs from the beginning
    playlist_songs_by_pos = dict(map(
        lambda x: (int(x['pos']), x),
        c.playlistid()
    ))
    current_song_no = int(c.status()['song'])

    main_print(main, "removing:")
    for i in xrange(current_song_no):
        main_print(main, playlist_songs_by_pos[0]['file'])
        c.delete(0)

    # 2) add new songs at the bottom
    playlist_songs = dict(map(lambda x: (x['file'], x), c.playlistid()))
    all_songs = dict(map(lambda x: (x['file'], x), c.search("file", "")))

    new_files = list(set(all_songs).difference(playlist_songs))
    new_files = new_files[0:max(0, PLAYLIST_LENGTH - len(playlist_songs))]
    random.shuffle(new_files)

    main_print(main, "adding:")
    for thefile in new_files:
        main_print(main, thefile)
        c.add(thefile)

    c.disconnect()

if __name__ == "__main__":
    import django
    django.setup()
    update_playlist(main=True)
