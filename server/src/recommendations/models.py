# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import CourseUser

class Day(models.Model):
    day = models.CharField(max_length=10, unique=True)

    def toJSON(self):
        return {
            "id": self.id,
            "day": self.day
        }

class Time(models.Model):
    start = models.TimeField(unique=True)
    end = models.TimeField(unique=True)

    def toJSON(self):
        return {
            "id": self.id,
            "start": {
                "time": self.start,
                "hour": self.start.hour
            },
            "end": {
                "time": self.end,
                "hour": self.end.hour
            }
        }

class Availability(models.Model):
    course_user = models.ForeignKey(CourseUser)
    day = models.ForeignKey(Day)
    time = models.ForeignKey(Time)

    def toJSON(self):
        return {
            "id": self.id,
            "courseUser": self.course_user.toJSON(),
            "day": self.day.toJSON(),
            "time": self.time.toJSON()
        }
