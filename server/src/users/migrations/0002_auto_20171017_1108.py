# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-17 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='roles',
            field=models.ManyToManyField(to='users.Role'),
        ),
    ]
