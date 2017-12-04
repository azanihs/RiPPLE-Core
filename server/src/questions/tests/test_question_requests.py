# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from questions.models import Topic, Distractor, Question, QuestionResponse, QuestionScore, Competency
from questions.services import AuthorService
from users.models import CourseUser
from django.db import IntegrityError

from .common import BootstrapTestCase

class QuestionRequestTest(BootstrapTestCase):

    def test_add_question(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        new_question = self._bootstrap_question_request()

        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Question Added")
    
    def test_none_field(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)

        attributes = ["question", "explanation", "responses", "topics"]

        for i in attributes:
            new_question = self._bootstrap_question_request()
            new_question[i] = None
            response = AuthorService.add_question(new_question, "/", author)
            self.assertEqual(response["state"], "Error")
        
        new_question = self._bootstrap_question_request()
        for key in new_question["responses"]:
            new_question["responses"][key] = None
        response = AuthorService.add_question(new_question, "/", author)
        self.assertEqual(response["state"], "Error")

    def test_check_for_script_tags(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        
        attributes = ["question", "explanation"]

        script_tag = "<script> evil code </script>"

        for attribute in attributes:
            new_question = self._bootstrap_question_request()
            new_question[attribute]["content"] = script_tag
            response = AuthorService.add_question(new_question, "/", author)
            self.assertEqual(response["state"], "Error")
        
        new_question = self._bootstrap_question_request()
        for key in new_question["responses"]:
            distractor = new_question["responses"][key]
            distractor["content"] = script_tag
            self.assertEqual(response["state"], "Error")
