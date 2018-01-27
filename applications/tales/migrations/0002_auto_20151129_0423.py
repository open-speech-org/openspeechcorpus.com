# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20151120_1308'),
        ('tales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaleVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calification', models.DecimalField(max_digits=3, decimal_places=2)),
                ('opinion', models.TextField(null=True, blank=True)),
                ('anonymous_user', models.ForeignKey(to='authentication.AnonymousUserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='tale',
            name='calification',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2),
        ),
        migrations.AddField(
            model_name='tale',
            name='total_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='talevote',
            name='tale',
            field=models.ForeignKey(to='tales.Tale'),
        ),
    ]
