# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-08 04:38
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
            name='Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.FloatField()),
                ('confidence', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Distractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('response', models.CharField(max_length=1)),
                ('isCorrect', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='DistractorImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='question_photo')),
                ('distractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Distractor')),
            ],
        ),
        migrations.CreateModel(
            name='ExplanationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='question_photo')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('explanation', models.TextField()),
                ('difficulty', models.FloatField()),
                ('quality', models.FloatField()),
                ('difficultyCount', models.IntegerField()),
                ('qualityCount', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='question_photo')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.FloatField(null=True)),
                ('difficulty', models.FloatField(null=True)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Distractor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Distractor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('number_answers', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='ReportQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='ReportQuestionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_text', models.TextField()),
                ('report_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.ReportQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='ReportReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course')),
            ],
        ),
        migrations.AddField(
            model_name='reportquestionlist',
            name='report_reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.ReportReason'),
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(to='questions.Topic'),
        ),
        migrations.AddField(
            model_name='explanationimage',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question'),
        ),
        migrations.AddField(
            model_name='distractor',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question'),
        ),
        migrations.AddField(
            model_name='competency',
            name='topics',
            field=models.ManyToManyField(to='questions.Topic'),
        ),
        migrations.AddField(
            model_name='competency',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CourseUser'),
        ),
    ]
