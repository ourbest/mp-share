# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-05 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170505_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxclick',
            name='uuid',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='wxshareurl',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
    ]