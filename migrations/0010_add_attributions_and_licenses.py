# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0009_use_only_song_model_for_referencing_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playedsong',
            name='song',
        ),
        migrations.DeleteModel(
            name='PlayedSong',
        ),
        migrations.RemoveField(
            model_name='playlistvote',
            name='song',
        ),
        migrations.DeleteModel(
            name='PlaylistVote',
        ),
        migrations.RemoveField(
            model_name='songfav',
            name='song',
        ),
        migrations.DeleteModel(
            name='SongFav',
        ),
        migrations.RemoveField(
            model_name='songrequest',
            name='song',
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
            name='Attribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(help_text=b'matches on the start of the string(i.e. "artist" matches "artist/song.mp3", but not "artist2/artist.mp3")', unique=True, max_length=2048)),
                ('artist', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(blank=True)),
                ('text', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayedSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(to='mpdsongvote.Song')),
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
                ('song', models.ForeignKey(to='mpdsongvote.Song')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SongFav',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(to='mpdsongvote.Song')),
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
                ('song', models.ForeignKey(to='mpdsongvote.Song')),
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
        migrations.AddField(
            model_name='attribution',
            name='license',
            field=models.ForeignKey(to='mpdsongvote.License'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='attribution',
            field=models.ForeignKey(default=None, blank=True, to='mpdsongvote.Attribution', null=True),
            preserve_default=True,
        ),
    ]
