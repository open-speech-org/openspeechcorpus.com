# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_audiodata_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiodata',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
