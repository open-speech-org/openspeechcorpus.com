# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_anonymoususerprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUserProfileHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('anonymous_name', models.CharField(max_length=100, null=True, blank=True)),
                ('anonymous_picture', models.ImageField(null=True, upload_to=b'anonymous_pictures', blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='anonymoususerprofile',
            name='anonymous_picture',
            field=models.ImageField(null=True, upload_to=b'anonymous_pictures', blank=True),
        ),
        migrations.AddField(
            model_name='anonymoususerprofilehistory',
            name='anonymous_user_profile',
            field=models.ForeignKey(to='authentication.AnonymousUserProfile'),
        ),
    ]
