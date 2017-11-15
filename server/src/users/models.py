# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz as timezone
from django.db import models


class Course(models.Model):
    course_code = models.CharField(max_length=30)
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
            "start": self.start.replace(tzinfo=timezone.utc).timestamp() if self.start else None,
            "end": self.end.replace(tzinfo=timezone.utc).timestamp() if self.end else None
        }


class User(models.Model):
    user_id = models.CharField(max_length=30)
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

    def toJSON(self):
        return {
            "user": self.user.toJSON(),
            "course": self.course.toJSON(),
            "roles": [str(x) for x in self.roles.all()]
        }


class Token(models.Model):
    payload = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CourseUser)
