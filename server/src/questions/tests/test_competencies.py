# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from questions.models import Topic, Distractor, Question, QuestionResponse, QuestionScore, Competency
from questions.services import CompetencyService, QuestionService, SearchService
from users.models import CourseUser
from ripple.util.util import combinations

from .common import BootstrapTestCase

class CompetencyTestCase(BootstrapTestCase):
    def test_answer_many_correct_questions_single_topic(self):
        """ checks that answering many correct questions bring competency upwards"""
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)

        topic_selected = Topic.objects.all().filter(id__in=[1])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(2, author)

        for i in range(1, 20):
            offset = 4 * i
            old_competency = Competency.objects.all().first().competency
            QuestionService.respond_to_question(2 + offset, author)
            new_competency = Competency.objects.all().first().competency
            self.assertTrue(old_competency <= new_competency)
        self.assertEqual(QuestionResponse.objects.count(), 20)
        self.assertEqual(Competency.objects.count(), 1)


    def test_answer_many_incorrect_questions_single_topic(self):
        """ checks that answering a question incorrectly does not store competency """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        # Answer question incorrectly
        QuestionService.respond_to_question(3, author)
        for i in range(1, 20):
            offset = 4 * i
            old_competency = Competency.objects.all().first().competency
            # Answer another question incorrectly
            QuestionService.respond_to_question(3 + offset, author)
            new_competency = Competency.objects.all().first().competency
            self.assertTrue(old_competency >= new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)
        self.assertEqual(Competency.objects.count(), 1)

    def test_answer_many_correct_questions_many_topics(self):
        """ check that answering many correct questions affects competency children """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1, 2])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(2, author)

        for i in range(1, 20):
            offset = 4 * i
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency
            QuestionService.respond_to_question(2 + offset, author)
            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertTrue(first_old_competency <= first_new_competency)
            self.assertTrue(second_old_competency <= second_new_competency)
            self.assertTrue(third_old_competency <= third_new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)

        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answer_many_incorrect_questions_many_topics(self):
        """ check that answering many incorrect questions affects competency children"""
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1, 2])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(3, author)

        for i in range(1, 20):
            offset = 4 * i
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency
            QuestionService.respond_to_question(3 + offset, author)
            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertTrue(first_old_competency >= first_new_competency)
            self.assertTrue(second_old_competency >= second_new_competency)
            self.assertTrue(third_old_competency >= third_new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)

        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answer_alternating_questions_many_topics(self):
        """ answer alternating questions to ensure competency scores bounce accordingly """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1, 2])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        # Get question wrong
        QuestionService.respond_to_question(2, author)
        for i in range(1, 10):
            offset = (4 * i) + (4 * (i - 1))
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency

            # Get question wrong
            QuestionService.respond_to_question(3 + offset, author)

            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertTrue(first_old_competency >= first_new_competency)
            self.assertTrue(second_old_competency >= second_new_competency)
            self.assertTrue(third_old_competency >= third_new_competency)

            QuestionService.respond_to_question(2 + offset, author)

            self.assertTrue(first_new_competency <= Competency.objects.all()[0].competency)
            self.assertTrue(second_new_competency <= Competency.objects.all()[1].competency)
            self.assertTrue(third_new_competency <= Competency.objects.all()[2].competency)

        self.assertEqual(QuestionResponse.objects.count(), 19)

        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answer_question_different_difficulties(self):
        """ Test for checking that difficulty influences competency scores """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        responder_user = self._bootstrap_user(2)
        responder = CourseUser.objects.create(user = responder_user, course=author_course)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)

        for question in Question.objects.all():
            question.difficulty = 10
            question.save()

        topic_selected = Topic.objects.all().filter(id__in=[2])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        starting_point = 20 * 4

        QuestionService.respond_to_question(2, author)
        QuestionService.respond_to_question(2 + starting_point, responder)

        for i in range(1, 20):
            offset = 4 * i
            author_old_competency = Competency.objects.get(user = author).competency
            responder_old_competency = Competency.objects.get(user = responder).competency

            QuestionService.respond_to_question(2 + offset, author)
            QuestionService.respond_to_question((2 + starting_point) + offset, responder)

            author_new_competency = Competency.objects.get(user = author).competency
            responder_new_competency = Competency.objects.get(user = responder).competency

            self.assertTrue(author_old_competency <= author_new_competency)
            self.assertTrue(responder_old_competency <= responder_new_competency)
            self.assertTrue(author_new_competency >= responder_new_competency)

    def test_decay_function(self):
        """ Test decay function influences question competency over time """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        responder_user = self._bootstrap_user(2)
        responder = CourseUser.objects.create(user = responder_user, course=author_course)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        topic_selected = Topic.objects.all().filter(id__in=[1])
        self._bootstrap_questions_same_topics(author, topic_selected, 20)
        self._bootstrap_question_choices(correct_id=2)

        for question in Question.objects.all():
            question.difficulty = 10
            question.save()

        for i in range(0,10):
            offset = 4 * i
            QuestionService.respond_to_question(2 + offset, author)
            QuestionService.respond_to_question(3 + offset, responder)      
        for i in range(10,20):
            offset = 4 * i
            QuestionService.respond_to_question(3 + offset, author)            
            QuestionService.respond_to_question(2 + offset, responder)

        author_competency = Competency.objects.get(user = author).competency
        responder_competency = Competency.objects.get(user = responder).competency
        self.assertEqual(QuestionResponse.objects.count(), 40)
        self.assertEqual(QuestionScore.objects.count(), 40)
        self.assertTrue(author_competency <= responder_competency)
