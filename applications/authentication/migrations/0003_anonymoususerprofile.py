# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20151030_0507'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anonymous_name', models.CharField(max_length=100)),
            ],
        ),
    ]
