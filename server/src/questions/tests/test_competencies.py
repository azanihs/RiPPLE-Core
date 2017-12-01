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
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(2, author)
        for i in range(0, 19):
            old_competency = Competency.objects.all().first().competency
            QuestionService.respond_to_question(2, author)
            new_competency = Competency.objects.all().first().competency
            self.assertLess(old_competency, new_competency)
        self.assertEqual(QuestionResponse.objects.count(), 20)
        self.assertEqual(Competency.objects.count(), 1)


    def test_answer_many_incorrect_questions_single_topic(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(3, author)
        for i in range(0, 19):
            old_competency = Competency.objects.all().first().competency
            QuestionService.respond_to_question(3, author)
            new_competency = Competency.objects.all().first().competency
            self.assertGreater(old_competency, new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)
        self.assertEqual(Competency.objects.count(), 1)

    def test_answer_many_correct_questions_many_topics(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(6, author)
        for i in range(0, 19):
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency
            QuestionService.respond_to_question(6, author)
            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertLess(first_old_competency, first_new_competency)
            self.assertLess(second_old_competency, second_new_competency)
            self.assertLess(third_old_competency, third_new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)

        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answer_many_incorrect_questions_many_topics(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(7, author)
        for i in range(0, 19):
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency
            QuestionService.respond_to_question(7, author)
            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertGreater(first_old_competency, first_new_competency)
            self.assertGreater(second_old_competency, second_new_competency)
            self.assertGreater(third_old_competency, third_new_competency)

        self.assertEqual(QuestionResponse.objects.count(), 20)
        
        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answer_alternating_questions_many_topics(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        QuestionService.respond_to_question(7, author)
        for i in range(0, 9):
            first_old_competency = Competency.objects.all()[0].competency
            second_old_competency = Competency.objects.all()[1].competency
            third_old_competency = Competency.objects.all()[2].competency

            QuestionService.respond_to_question(6, author)

            first_new_competency = Competency.objects.all()[0].competency
            second_new_competency = Competency.objects.all()[1].competency
            third_new_competency = Competency.objects.all()[2].competency
            self.assertLess(first_old_competency, first_new_competency)
            self.assertLess(second_old_competency, second_new_competency)
            self.assertLess(third_old_competency, third_new_competency)

            QuestionService.respond_to_question(7, author)

            self.assertGreater(first_new_competency, Competency.objects.all()[0].competency)
            self.assertGreater(second_new_competency, Competency.objects.all()[1].competency)
            self.assertGreater(third_new_competency, Competency.objects.all()[2].competency)

        self.assertEqual(QuestionResponse.objects.count(), 19)
        
        num_topics = combinations(QuestionScore.objects.all().first().question.topics.all())
        self.assertEqual(Competency.objects.count(), len(num_topics))

    def test_answering_question_different_difficulties(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        responder_user = self._bootstrap_user(2)
        responder = CourseUser.objects.create(user = responder_user, course=author_course)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        question = Question.objects.all().first()
        question.difficulty = 10
        question.save()

        QuestionService.respond_to_question(2, author)
        QuestionService.respond_to_question(14, responder)        

        for i in range(0, 19):
            author_old_competency = Competency.objects.get(user = author).competency
            responder_old_competency = Competency.objects.get(user = responder).competency

            QuestionService.respond_to_question(2, author)
            QuestionService.respond_to_question(14, responder)

            author_new_competency = Competency.objects.get(user = author).competency
            responder_new_competency = Competency.objects.get(user = responder).competency

            self.assertLess(author_old_competency, author_new_competency)
            self.assertLess(responder_old_competency, responder_new_competency)
            self.assertGreater(author_new_competency, responder_new_competency)
  

    def astest_1(self):
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        for i in Question.objects.all():
            i.difficulty = 10
            print(i.difficulty)
            i.save()

        for i in range(0, 20):
            print("TRUE " + str(i))
            QuestionService.respond_to_question(6, author)
            print("First: " + str(Competency.objects.all()[0]))
            print("SECOND: " + str(Competency.objects.all()[1]))
            print("THIRD: " + str(Competency.objects.all()[2]))
            
            # print("FALSE")
            # QuestionService.respond_to_question(6, author)
            # print("First: " + str(Competency.objects.all()[0]))
            # print("SECOND: " + str(Competency.objects.all()[1]))
            # print("THIRD: " + str(Competency.objects.all()[2]))
            # print("TRUE")
            # QuestionService.respond_to_question(6, author)
            # print("First: " + str(Competency.objects.all()[0]))
            # print("SECOND: " + str(Competency.objects.all()[1]))
            # print("THIRD: " + str(Competency.objects.all()[2]))
            print("-------------")
