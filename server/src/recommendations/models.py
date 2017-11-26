# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import CourseUser
from questions.models import Topic

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
            "course_user": self.course_user.toJSON(),
            "day": self.day.toJSON(),
            "time": self.time.toJSON()
        }

class StudyRole(models.Model):
    role = models.CharField(max_length=32)

    def __str__(self):
        return str(self.role)

    def toJSON(self):
        return {
            "id": self.id,
            "role": self.role
        }

class AvailableRole(models.Model):
    course_user = models.ForeignKey(CourseUser)
    topic = models.ForeignKey(Topic)
    study_role = models.ForeignKey(StudyRole)

    def toJSON(self):
        return {
            "course_user": self.course_user.toJSON(),
            "topic": self.topic.toJSON(),
            "studyRole": self.study_role.toJSON()
        }
