# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import CourseUser

class Day(models.Model):
    day = models.CharField(max_length=10, unique=True)

    def toJSON(self):
        return {
            "day": self.day
        }

class Time(models.Model):
    start = models.TimeField(unique=True)
    end = models.TimeField(unique=True)

    def toJSON(self):
        return {
            "start": self.start,
            "end": self.end
        }

class Availability(models.Model):
    course_user = models.ForeignKey(CourseUser)
    day = models.ForeignKey(Day)
    time = models.ForeignKey(Time)

    def toJSON(self):
        return {
            "course_user": self.course_user.toJSON(),
            "day": self.day.toJSON(),
            "time": self.time.toJSON()
        }
