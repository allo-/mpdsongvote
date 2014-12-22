from models import *
from util import *
from django.db import models


NUM_RECENTLY_PLAYED = 5
NUM_RECENTLY_REQUESTED = 5


def recently_played(request):
    # list of last NUM_RECENTLY_PLAYED recently played songs
    rp = PlayedSong.objects.all().order_by("-id")[:NUM_RECENTLY_PLAYED].values()
    add_num_requests_to_songlist(rp)
    return {
        'recently_played': rp
    }


def recently_requested(request):
    sr = SongRequest.objects.order_by("-date")[:NUM_RECENTLY_REQUESTED].values()
    add_num_requests_to_songlist(sr)
    return {
        'recently_requested': sr
    }


def most_wanted(request):
    sr = SongRequest.objects.annotate(
        votes=models.Sum("songrequestvote__value")
    ).order_by("-votes")[:NUM_RECENTLY_REQUESTED].values()
    add_num_requests_to_songlist(sr)
    return {
        'most_wanted': sr
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
