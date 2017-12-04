# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from django.utils import timezone
import datetime
from django.test import TestCase
from questions.models import Topic, Question, Distractor, Competency
from users.models import User, Role, Course, CourseUser


class BootstrapTestCase(TestCase):
    def _bootstrap_courses(self, id):
        return Course.objects.create(course_code="test_course_" + str(id), 
            course_name="course_name_" + str(id),
            start=timezone.now() - datetime.timedelta(days=5),
            end=timezone.now(),
            available=True)

    def _bootstrap_user(self):
        user = User(user_id="u_id", first_name="u_firstname", last_name="u_lastname")
        user.save()
        return user

    def _bootstrap_role(self, role):
        role = Role(role=role)
        role.save()
        return role

    def _bootstrap_course_user(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user()
        cu = CourseUser(course=course, user=user)
        cu.save()
        return cu

    def _user_in_course(self, user, course):
        cu = CourseUser(course=course, user=user)
        cu.save()
        return cu

    def _bootstrap_topics(self, course):
        return [Topic.objects.create(name=x, course=course)
         for x in ["t1", "t2", "t3", "t4", "t5", "t6"]]

    def _bootstrap_competencies(self, user, topics):
        c = Competency(
            competency = 100,
            confidence = 100,
            user = user
        )
        c.save()
        if isinstance(topics, list):
            c.topics.set(topics)
        else:
            c.topics.set([topics])
        return c

