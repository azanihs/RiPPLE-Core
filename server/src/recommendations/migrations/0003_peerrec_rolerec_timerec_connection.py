# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-11 04:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171208_0955'),
        ('recommendations', '0002_studyrole_availablerole'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_status', models.CharField(max_length=20)),
                ('recommended_user_status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PeerRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_user', to='users.CourseUser')),
                ('recommended_course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_course_user', to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='RoleRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peer_recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.PeerRecommendation')),
                ('recomended_user_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user_role', to='recommendations.AvailableRole')),
                ('user_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='recommendations.AvailableRole')),
            ],
        ),
        migrations.CreateModel(
            name='TimeRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peer_recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.PeerRecommendation')),
                ('recommended_user_availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user_availability', to='recommendations.Availability')),
                ('user_availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_availability', to='recommendations.Availability')),
            ],
        ),
        migrations.AddField(
            model_name='connection',
            name='peer_recommendation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.PeerRecommendation'),
        ),
        migrations.AddField(
            model_name='connection',
            name='role_recommendation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.RoleRecommendation'),
        ),
        migrations.AddField(
            model_name='connection',
            name='time_recommendation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.TimeRecommendation'),
        ),
    ]
