You need to change ```TEMPLATE_CONTEXT_PROCESSORS```:
- add the [default context processors](https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS) from django
- add ```django.core.context_processors.request```
- add ```mpdsongvote.context_processors.mpdsongvote```

To update the playlist even when nobody is voting, you need to run via cron:
```DJANGO_SETTINGS_MODULE="yourproject.settings" python update_playlist.py```. The interval should be smaller than the playtime of two songs.
