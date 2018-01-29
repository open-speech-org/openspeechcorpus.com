# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_audiodata_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CommandCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CommandSpeech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio', models.ForeignKey(to='core.AudioData', on_delete=models.CASCADE)),
                ('command', models.ForeignKey(to='miscellany.Command', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='category',
            field=models.ManyToManyField(to='miscellany.CommandCategory'),
        ),
    ]
