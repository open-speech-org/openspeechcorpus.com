# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_anonymoususerprofile'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousAudioData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio', models.ForeignKey(to='core.AudioData', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to='authentication.AnonymousUserProfile', on_delete=models.CASCADE)),
            ],
        ),
    ]
