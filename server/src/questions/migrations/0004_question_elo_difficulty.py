# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_deletedquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='elo_difficulty',
            field=models.FloatField(default=1000),
        ),
    ]
