# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160115_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioDatasMigration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('new_user', models.ForeignKey(related_name='new_user', to='core.AnonymousAudioData', on_delete=models.CASCADE)),
                ('old_user', models.ForeignKey(related_name='old_user', to='core.AnonymousAudioData', on_delete=models.CASCADE)),
            ],
        ),
    ]
