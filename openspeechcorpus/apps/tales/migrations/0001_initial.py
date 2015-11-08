# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('biography', models.TextField(null=True, blank=True)),
                ('birth', models.DateField(null=True, blank=True)),
                ('death', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SentenceTaleSpeech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio', models.ForeignKey(to='core.AudioData')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('starts', models.DateField(null=True, blank=True)),
                ('ends', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(to='tales.Author')),
            ],
        ),
        migrations.CreateModel(
            name='TaleSentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('text', models.TextField()),
                ('tale', models.ForeignKey(to='tales.Tale')),
            ],
        ),
        migrations.AddField(
            model_name='sentencetalespeech',
            name='tale_sentence',
            field=models.ForeignKey(to='tales.TaleSentence'),
        ),
        migrations.AddField(
            model_name='author',
            name='styles',
            field=models.ManyToManyField(to='tales.Style', null=True, blank=True),
        ),
    ]
