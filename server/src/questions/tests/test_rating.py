# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questions.models import Question, QuestionRating
from questions.services import QuestionService
from users.models import CourseUser

from .common import BootstrapTestCase

class RatingTest(BootstrapTestCase):

    def test_rate_nonexistent(self):
        """ Tests rating a question which does not exists """
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)
        self.assertFalse(QuestionService.rate_question(-1, { "difficulty": 2, "quality": 4}, author))

    def test_new_rate(self):
        """ Tests rating a question which the user has not rated before """
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        self.assertTrue(QuestionService.rate_question(2, { "difficulty": 2, "quality": 4}, author))
        user_rating = QuestionRating.objects.all()
        self.assertEqual(len(user_rating), 1)
        self.assertEqual(user_rating.first().quality, 4.0)
        self.assertEqual(user_rating.first().difficulty, 2.0)

        answered_question = Question.objects.get(pk=1).toJSON()
        self.assertEqual(answered_question["difficultyCount"], 1)
        self.assertEqual(answered_question["difficulty"], 2.0)

    def test_rate_update(self):
        """ Tests rating a question which the user has rated before"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)
        QuestionService.rate_question(2, { "difficulty": 2, "quality": 4 }, author)
        self.assertTrue(QuestionService.rate_question(2, { "difficulty": 4 }, author))

        user_rating = QuestionRating.objects.all()
        self.assertEqual(len(user_rating), 1)
        self.assertEqual(user_rating.first().quality, 4.0)
        self.assertEqual(user_rating.first().difficulty, 4.0)

        answered_question = Question.objects.get(pk=1).toJSON()
        self.assertEqual(answered_question["difficultyCount"], 1)
        self.assertEqual(answered_question["difficulty"], 4.0)

    def test_rate_many(self):
        """ Tests rating a question with many users"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)

        user2 = self._bootstrap_user(2)
        author2 = CourseUser.objects.create(user=user2, course=course)

        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.rate_question(1, { "quality": 2 }, author)
        QuestionService.rate_question(1, { "quality": 2 }, author2)
        QuestionService.rate_question(1, { "quality": 4 }, author2)

        answered_question = Question.objects.get(pk=1).toJSON()
        self.assertEqual(answered_question["qualityCount"], 2)
        self.assertEqual(answered_question["quality"], 3.0)
