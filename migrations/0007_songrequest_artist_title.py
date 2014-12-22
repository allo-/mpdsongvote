# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0006_songrequest_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='songrequest',
            name='artist',
            field=models.CharField(default='unknown artist', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='songrequest',
            name='title',
            field=models.CharField(default='unknown title', max_length=255),
            preserve_default=False,
        ),
    ]
