# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from questions.models import Topic, Distractor, Question, QuestionResponse, QuestionScore, Competency
from questions.services import SearchService
from users.models import CourseUser

from .common import BootstrapTestCase

class SearchServiceTestCase(BootstrapTestCase):
    def test_search_service_constructor(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)

        try:
            test_search = SearchService.SearchService(course)
        except Exception as e:
            self.fail("Search constructor raised exception:  " + str(e))

        #Checking the query returns all the questions created = 5
        num_questions = Question.objects.count()
        self.assertEqual(num_questions, test_search.execute().count())

    def test_topic_filter_single_topic(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)

        test_search = SearchService.SearchService(course)
        topic = Topic.objects.filter(name = "t1")
        filtered_questions = Question.objects.filter(topics__in = topic)
        test_search.add_topic_filter(topic)
        for i in test_search.execute():
            self.assertTrue(i in filtered_questions)

        #In common.py 2 questions are defined with topic t2
        self.assertEqual(test_search.execute().count(), 2)

    def test_topic_filter_many_topics(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)

        test_search = SearchService.SearchService(course)
        topic = Topic.objects.filter(name__in = ["t2", "t3", "t4"])
        filtered_questions = Question.objects.filter(topics__in = topic)
        test_search.add_topic_filter(topic)
        for i in test_search.execute():
            self.assertTrue(i in filtered_questions)

        #In common.py 4 questions are defined with topic t2, t3, or t4
        self.assertEqual(test_search.execute().count(), 4)

    def test_text_search(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        test_search = SearchService.SearchService(course)

        Question.objects.all()[0].content = "look for this"
        Question.objects.all()[1].content = "look for this"
        Question.objects.all()[2].content = "look for this"
        print(Question.objects.all()[0].content)
        test_search.text_search("look for this")
        searched_questions = test_search.execute()

        for i in searched_questions:
            self.assertTrue(i in Question.objects.all()[0:3])
        self.assertEqual(test_search.execute().count(), 3)
        
