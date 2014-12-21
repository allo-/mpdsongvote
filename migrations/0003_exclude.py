# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0002_playlistitem_playlistvote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exclude',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(default=0, max_length=20, choices=[(b'file', b'filename'), (b'title', b'title'), (b'artist', b'artist')])),
                ('value', models.CharField(unique=True, max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
