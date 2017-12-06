# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from questions.models import Topic, Question, QuestionResponse, QuestionScore
from questions.services import SearchService, QuestionService
from users.models import CourseUser

from .common import BootstrapTestCase

class SearchServiceTestCase(BootstrapTestCase):
    def test_search_service_constructor(self):
        """Test the creation of a search service raises no exceptions"""
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
        """Test that filtering trough a single topic gives only questions that contain that topic"""
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
        """Test that filtering with many topics give all the questions that contain any of those topics"""
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
        """Check that questions can be filtered by content text search"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        test_search = SearchService.SearchService(course)

        #Change content on the first 3 questions
        num_test_questions = 3
        for i in range(0,num_test_questions):
            question_to_change = Question.objects.all()[i]
            question_to_change.content = "look for this"
            question_to_change.save()

        test_search.text_search("look for this")
        searched_questions = test_search.execute()

        for i in searched_questions:
            self.assertTrue(i in Question.objects.all()[0:num_test_questions])
        self.assertEqual(test_search.execute().count(), num_test_questions)
        

    def test_add_filter_unanswered(self):
        """Test that questions are filtered when they have not been answered before, no QuestionResponse"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        #answer the first two questions
        QuestionService.respond_to_question(2, author)
        QuestionService.respond_to_question(6, author)

        test_search = SearchService.SearchService(course)
        test_search.add_filter("unanswered", author)
        unanswered_questions = test_search.execute()

        # Check searched questions should be the last 3 unanaswered ones
        for i in unanswered_questions:
            self.assertTrue(i in Question.objects.all()[2:5])
        self.assertEqual(test_search.execute().count(), 3)


    def test_add_filter_answered(self):
        """test that questions can be filtered if they have been answered before, QuestionResponse exists"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        #answer the first two questions
        QuestionService.respond_to_question(2, author)
        QuestionService.respond_to_question(6, author)

        test_search = SearchService.SearchService(course)
        test_search.add_filter("answered", author)
        answered_questions = test_search.execute()

        # Check searched questions should be the first 2 answered ones        
        for i in answered_questions:
            self.assertTrue(i in Question.objects.all()[0:2])
        self.assertEqual(test_search.execute().count(), 2)


    def test_add_filter_improve(self):
        """
            Test that questions can be filtered by questions answered where user did not get maximun score. 
            QuestionResponse exists but Question Score < 1
        """
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        #answer the first question correctly after two tries
        QuestionService.respond_to_question(3, author)
        QuestionService.respond_to_question(2, author)
        
        test_search = SearchService.SearchService(course)
        test_search.add_filter("improve", author)
        improve_questions = test_search.execute()
    
        self.assertEqual(Question.objects.all().first(), improve_questions.first())
        self.assertEqual(test_search.execute().count(), 1)