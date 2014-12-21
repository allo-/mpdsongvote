from models import *


NUM_RECENTLY_PLAYED = 5


def recently_played(request):
    return {
        'recently_played':
            PlayedSong.objects.all().order_by("-id")[:NUM_RECENTLY_PLAYED]
    }


def mpdsongvote(request):
    items = {}

    new_items = recently_played(request)
    for item in new_items:
        items[item] = new_items[item]
    return items
