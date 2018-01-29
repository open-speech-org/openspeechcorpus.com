# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('reverse_lazy_url', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_token', models.CharField(max_length=40, blank=True)),
                ('expiration', models.DateTimeField(null=True, blank=True)),
                ('role', models.ForeignKey(to='authentication.Role', on_delete=models.CASCADE)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.RemoveField(
            model_name='activationtoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='ActivationToken',
        ),
        migrations.AddField(
            model_name='permission',
            name='role',
            field=models.ManyToManyField(to='authentication.Role'),
        ),
    ]
