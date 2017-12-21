# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz as timezone
from datetime import datetime
from django.db import models

_epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

class Course(models.Model):
    course_code = models.CharField(max_length=30, unique=True)
    course_name = models.CharField(max_length=30)
    available = models.BooleanField(default=False)

    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toJSON(self):
        return {
            "courseCode": self.course_code,
            "courseName": self.course_name,
            "available": self.available,
            "start": (self.start.replace(tzinfo=timezone.utc) - _epoch).total_seconds() if self.start else None,
            "end": (self.end.replace(tzinfo=timezone.utc) - _epoch).total_seconds() if self.end else None
        }


class User(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toJSON(self):
        return {
            "name": self.first_name + " " + self.last_name,
            "image": self.image
        }


class UserImage(models.Model):
    image = models.ImageField(upload_to='user_photo')
    user = models.ForeignKey(User, on_delete=None)

class Role(models.Model):
    role = models.CharField(max_length=32)

    def __str__(self):
        return str(self.role)


class CourseUser(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    roles = models.ManyToManyField(Role)

    elo_rating = models.FloatField(default=1000)

    def toJSON(self):
        return {
            "user": self.user.toJSON(),
            "course": self.course.toJSON(),
            "roles": [str(x) for x in self.roles.all()]
        }

    class Meta:
        unique_together = ('user', 'course')


class Token(models.Model):
    payload = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CourseUser)


class Notification(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    icon = models.CharField(default="Bronze", max_length=30)

    user = models.ForeignKey(CourseUser)

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "created": (self.created.replace(tzinfo=timezone.utc) - _epoch).total_seconds()
        }

class Engagement(models.Model):
    name = models.CharField(max_length=64)
    course = models.ForeignKey(Course)
    model = models.CharField(max_length=32)
    filter_name = models.CharField(max_length=32)
    key_user = models.CharField(max_length=32)


    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name
        }
class ConsentForm(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(CourseUser)

    def toJSON(self):
        return {
            "content": self.content,
            "author": self.author.toJSON()
        }


class Consent(models.Model):
    user = models.ForeignKey(CourseUser)
    form = models.ForeignKey(ConsentForm)
    response = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class ConsentImage(models.Model):
    image = models.ImageField(upload_to='consent_images')
    form = models.ForeignKey(ConsentForm, on_delete=None)
