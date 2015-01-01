# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0008_song_songfav'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlayedSong',
        ),
        migrations.RemoveField(
            model_name='playlistvote',
            name='playlistitem',
        ),
        migrations.DeleteModel(
            name='PlaylistItem',
        ),
        migrations.DeleteModel(
            name='PlaylistVote',
        ),
        migrations.RemoveField(
            model_name='songrequestvote',
            name='songrequest',
        ),
        migrations.DeleteModel(
            name='SongRequest',
        ),
        migrations.DeleteModel(
            name='SongRequestVote',
        ),
        migrations.CreateModel(
            name='PlayedSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(to='mpdsongvote.Song', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
                ('song', models.ForeignKey(to='mpdsongvote.Song', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SongRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('song', models.ForeignKey(to='mpdsongvote.Song', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SongRequestVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
                ('songrequest', models.ForeignKey(to='mpdsongvote.SongRequest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='songfav',
            name='song',
            field=models.ForeignKey(to='mpdsongvote.Song', null=True),
            preserve_default=True,
        ),
    ]
