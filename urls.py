from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from views import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^artist/$', artists, name="artists"),

    url(r'^album/$', albums, name="albums"),
    url(r'^album/(?P<album>[^/]*)/$', album_songs, name='album_songs'),

    url(r'^artist/(?P<artist>[^/]*)/$', artist_albums, name='artist_albums'),
    url(r'^artist/(?P<artist>[^/]*)/(?P<album>[^/]*)/$', artist_album_songs,
        name='artist_album_songs'),

    url(r'^playlist/vote/up/$', playlist_vote,
        {'up': True}, name="playlist_vote_up"),
    url(r'^playlist/vote/down/$', playlist_vote,
        {'up': False}, name="playlist_vote_down"),
    url(r'^fav/$', fav_song, name="fav_song"),

    url(r'^request/$', request_song, name="request_song"),

    url(r'^attribution/(?P<attribution_id>[0-9]*)/$', show_attribution, name="show_attribution"),

    url(r'^$', playlist, name="playlist"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
