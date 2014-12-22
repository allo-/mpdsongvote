# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0005_songrequest_songrequestvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='songrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 22, 0, 0, 0, 0, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
