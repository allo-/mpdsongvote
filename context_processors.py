from models import *
from util import *
from django.db import models


NUM_RECENTLY_PLAYED = 5
NUM_RECENTLY_REQUESTED = 5


def recently_played(request):
    # list of last NUM_RECENTLY_PLAYED recently played songs
    rp = PlayedSong.objects.annotate(
        votes=models.Sum("song__songrequest__songrequestvote__value")
    ).order_by("-id")[:NUM_RECENTLY_PLAYED]
    return {
        'recently_played_songs': rp
    }


def recently_requested(request):
    sr = SongRequest.objects.annotate(
        votes=models.Sum("songrequestvote__value")
    ).order_by("-date")[:NUM_RECENTLY_REQUESTED]
    return {
        'recent_song_requests': sr
    }


def most_wanted(request):
    sr = SongRequest.objects.annotate(
        votes=models.Sum("songrequestvote__value")
    ).order_by("-votes")[:NUM_RECENTLY_REQUESTED]
    return {
        'most_wanted_song_requests': sr
    }


def mpdsongvote(request):
    items = {}
    context_processors = (
        recently_played,
        recently_requested,
        most_wanted
    )

    for context_processor in context_processors:
        new_items = context_processor(request)
        for item in new_items:
            items[item] = new_items[item]

    return items
