# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-07 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('key', models.CharField(max_length=75, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(default='', max_length=75)),
                ('bonus', models.IntegerField(default=0)),
                ('condition', models.IntegerField(default=1)),
                ('icon', models.CharField(default='Bronze', max_length=30)),
                ('callback', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=30, unique=True)),
                ('achievements', models.ManyToManyField(to='rippleAchievements.Achievement')),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userachievements', to='rippleAchievements.Achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.CharField(max_length=30, unique=True)),
                ('url', models.CharField(default='/<django.db.models.fields.CharField>', max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='views',
            field=models.ManyToManyField(to='rippleAchievements.View'),
        ),
    ]
