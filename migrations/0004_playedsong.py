# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpdsongvote', '0003_exclude'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayedSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
