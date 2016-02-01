# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tales', '0002_auto_20151129_0423'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='talevote',
            unique_together=set([('tale', 'anonymous_user')]),
        ),
    ]
