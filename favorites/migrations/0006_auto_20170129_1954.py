# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0005_auto_20170129_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='permalink',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='url',
            field=models.CharField(default='', max_length=250),
        ),
    ]
