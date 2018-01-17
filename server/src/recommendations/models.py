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
            "id": self.id,
            "courseUser": self.course_user.toJSON(),
            "day": self.day.toJSON(),
            "time": self.time.toJSON()
        }

class StudyRole(models.Model):
    role = models.CharField(max_length=32)
    description = models.CharField(max_length=32)

    def __str__(self):
        return str(self.role)

    def toJSON(self):
        return {
            "id": self.id,
            "role": self.role,
            "description": self.description
        }

class Request(models.Model):
    course_user = models.ForeignKey(CourseUser)
    topic = models.ForeignKey(Topic)
    study_role = models.ForeignKey(StudyRole)

    def toJSON(self):
        return {
            "courseUser": self.course_user.toJSON(),
            "topic": self.topic.toJSON(),
            "studyRole": self.study_role.toJSON()
        }

class PeerRecommendation(models.Model):
    course_user = models.ForeignKey(CourseUser, related_name="course_user")
    recommended_course_user = models.ForeignKey(CourseUser, related_name="recommended_course_user")

    def toJSON(self):
        return {
            "courseUser": self.course_user.toJSON(),
            "recommendedCourseUser": self.recommended_course_user.toJSON()
        }

class RoleRecommendation(models.Model):
    peer_recommendation = models.ForeignKey(PeerRecommendation)
    user_request = models.ForeignKey(Request, related_name="user_request")
    recomended_user_request = models.ForeignKey(Request, related_name="recommended_user_request")

    def toJSON(self):
        return {
            "peerRecommendation": self.peer_recommendation.toJSON(),
            "userRequest": self.user_request.toJSON(),
            "recomendedUserRequest": self.recomended_user_request.toJSON()
        }

class TimeRecommendation(models.Model):
    peer_recommendation = models.ForeignKey(PeerRecommendation)
    user_availability = models.ForeignKey(Availability, related_name="user_availability")
    recommended_user_availability = models.ForeignKey(Availability, related_name="recommended_user_availability")

    def toJSON(self):
        return {
            "peerRecommendation": self.peer_recommendation.toJSON(),
            "userAvailability": self.user_availability.toJSON(),
            "recommendedUserAvailability": self.recommended_user_availability.toJSON()
        }

class Connection(models.Model):
    peer_recommendation = models.ForeignKey(PeerRecommendation)
    role_recommendation = models.ForeignKey(RoleRecommendation)
    time_recommendation = models.ForeignKey(TimeRecommendation)
    user_status = models.CharField(max_length=20)
    recommended_user_status = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def toJSON(self):
        return {
            "peerRecommendation": self.peer_recommendation.toJSON(),
            "roleRecommendation": self.role_recommendation.toJSON(),
            "timeRecommendation": self.time_recommendation.toJSON(),
            "userStatus": self.user_status.toJSON(),
            "recommendedUserStatus": self.recommended_user_status.toJSON(),
            "location": self.location.toJSON()
        }
