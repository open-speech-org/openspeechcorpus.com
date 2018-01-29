# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_audiodatasmigration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiodatasmigration',
            name='new_user',
            field=models.ForeignKey(related_name='new_user', to='authentication.AnonymousUserProfile', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='audiodatasmigration',
            name='old_user',
            field=models.ForeignKey(related_name='old_user', to='authentication.AnonymousUserProfile', on_delete=models.CASCADE),
        ),
    ]
