# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscellany', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='category',
            field=models.ManyToManyField(to='miscellany.CommandCategory', blank=True),
        ),
    ]
