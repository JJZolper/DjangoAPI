# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 19:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0004_auto_20170129_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='access_token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]