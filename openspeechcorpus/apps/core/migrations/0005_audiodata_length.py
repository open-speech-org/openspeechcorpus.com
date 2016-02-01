# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_verificationhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiodata',
            name='length',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=3),
        ),
    ]
