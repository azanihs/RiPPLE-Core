# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import math
from questions.models import Course, Topic, Question, Distractor, QuestionResponse, QuestionScore, Competency
from questions.services import QuestionService, SearchService
from users.models import CourseUser, User

from .common import BootstrapTestCase

class TopicsTest(BootstrapTestCase):
    def test_course_topics(self):
        """ Tests fetching topics for a course"""
        course = self._bootstrap_courses(1)
        self._bootstrap_topics(course)

        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_questions(author)

        course_topics = QuestionService.get_course_topics(course)
        self.assertEqual(len(course_topics), 6)

    def test_course_topics_multiple(self):
        """ Tests fetching topics for a course when there are multiple courses"""
        courses = [self._bootstrap_courses(1), self._bootstrap_courses(2)]
        for _c, course in enumerate(courses):
            self._bootstrap_topics(course)
            user = self._bootstrap_user(_c)
            author = CourseUser.objects.create(user=user, course=course)
            self._bootstrap_questions(author)

        def _e(s):
            return [x for x in s]

        course_topics = QuestionService.get_course_topics(courses[0])
        self.assertEqual(_e(course_topics), _e(Topic.objects.filter(course=courses[0])))

        course_topics = QuestionService.get_course_topics(courses[1])
        self.assertEqual(_e(course_topics), _e(Topic.objects.filter(course=courses[1])))
