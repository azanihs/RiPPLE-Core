# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from django.test import TestCase
from questions.models import Topic, Question, Distractor
from users.models import User, Role, Course, CourseUser

class BootstrapTestCase(TestCase):
    def _bootstrap_courses(self, id):
        return Course.objects.create(course_code="test_course_" + str(id), course_name="course_name_" + str(id))

    def _bootstrap_user(self):
        user = User(user_id="u_id", first_name="u_firstname", last_name="u_lastname")
        user.save()
        return user

    def _bootstrap_role(self, role):
        role = Role(role=role)
        role.save()
        return role

    def _bootstrap_course_user(self):
        cu = CourseUser(course=self._bootstrap_courses(1), user=self._bootstrap_user)
        cu.save()
        cu.roles.set(self._bootstrap_role)
        return cu