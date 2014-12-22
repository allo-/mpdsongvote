#!/usr/bin/env python
import random
import mpd
from mpdsongvote.models import *
from django.db import models


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
        title = playlist_songs_by_pos[i].get('title', 'unknown title')
        artist = playlist_songs_by_pos[i].get('artist', '')
        PlayedSong(
            title=title, artist=artist, filename=filename).save()
        main_print(main, filename)
        c.delete(0)
        PlaylistItem.objects.filter(filename=filename).delete()

    # 2) add new songs at the bottom
    playlist_songs = dict(map(lambda x: (x['file'], x), c.playlistid()))
    all_songs_dict = dict(map(
        lambda x: (x['file'], x),
        c.search("file", "")
    ))

    # generate a list of random files, which are not in the playlist
    # or request list
    random_files = list(set(all_songs_dict).difference(playlist_songs))
    random.shuffle(random_files)

    # filter files from exclude criteria
    files_to_remove = []
    for exclude in Exclude.objects.all():
        for i in xrange(len(random_files)):
            exclude_value = exclude.value.lower()
            song_value = all_songs_dict[random_files[i]].get(exclude.field, '').lower()
            if exclude_value in song_value:
                files_to_remove.append(random_files[i])
    random_files = list(set(random_files).difference(files_to_remove))

    # get requested files, but only until the playlist has PLAYLIST_LENGTH
    requests = SongRequest.objects.all().annotate(
        votes=models.Sum("songrequestvote__value")
    )[:max(0, PLAYLIST_LENGTH - len(playlist_songs))]

    # build a list of requested files ordered by the number of votes
    request_votes = [
        (x['filename'], x['votes'])
        for x in requests.values("filename", "votes")
    ]
    requested_files = map(
        lambda x: x[0],
        sorted(request_votes, key=lambda x: x[1], reverse=True)
    )

    # remove added requests
    for request in requests:
        request.delete()

    # final list of new files: requested_files + random_files
    random_files = list(set(random_files).difference(requested_files))
    new_files = requested_files + random_files
    # limit to PLAYLIST_LENGTH
    new_files = new_files[0:max(0, PLAYLIST_LENGTH - len(playlist_songs))]

    main_print(main, "adding:")
    for thefile in new_files:
        main_print(main, thefile)
        # clear votes by removing any existing PlaylistItems
        PlaylistItem.objects.filter("filename"=thefile).delete()
        c.add(thefile)

    if not client:
        c.disconnect()

if __name__ == "__main__":
    import django
    django.setup()
    update_playlist(main=True)
