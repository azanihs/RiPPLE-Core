# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import random
import math
from questions.models import Course, Topic, Question, Distractor, QuestionResponse, QuestionScore, Competency
from users.models import CourseUser, User
from questions.services import QuestionService



# Create your tests here.


class QuestionTestCase(TestCase):
    def _bootstrap_courses(self):
        return Course.objects.create(course_code="test_course_1", course_name="course_name")

    def _bootstrap_topics(self, course):
        [Topic(id=i, name=x, course=course).save()
         for i, x in enumerate(["t1", "t2", "t3", "t4", "t5", "t6"])]

    def _bootstrap_questions(self, author):
        topic_map = [
            Topic.objects.filter(id__in=[1]),
            Topic.objects.filter(id__in=[1, 2]),
            Topic.objects.filter(id__in=[2, 3, 4]),
            Topic.objects.filter(id__in=[4]),
            Topic.objects.filter(id__in=[2, 4])
        ]

        for i in range(0, 5):
            q = Question(
                id=i + 1,
                author=author,
                content="",
                explanation="",
                difficulty=i+1,
                quality=1,
                difficultyCount=1,
                qualityCount=1
            )
            q.save()
            q.topics.set(topic_map[i])

    def _bootstrap_question_choices(self, correct_id):
        question_count = Question.objects.all().count()
        for i in range(0, (4 * question_count)):
            id = i + 1
            Distractor(
                id=id,
                content="question " + str(i),
                response=chr(ord('A') + id % 4),
                isCorrect=id == correct_id,
                question_id=math.ceil(id / 4.0)
            ).save()

    def _bootstrap_user(self, id):
        user = User(id=id, first_name="u_firstname", last_name="u_lastname")
        user.save()
        return user

    def test_answering_new_question_single_topic(self):
        """ New question with single topic """
        course = self._bootstrap_courses()
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)
        # print("FIRST TEST\n")
        # for i in range(0, 20):
        #     QuestionService.respond_to_question(2, author)
        #     print(Competency.objects.all().first().confidence)
        #     print(Competency.objects.all().first().competency)
        #     QuestionService.respond_to_question(3, author)
        #     print(Competency.objects.all().first().competency)

        # for i in range(0, 20):
        #     QuestionService.respond_to_question(2, author)
        #     print(Competency.objects.all().first().competency)

    def test_answering_new_question_multiple_topics(self):
        """ New question with multiple topics """
        course = self._bootstrap_courses()
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=6)

        print("SECOND TEST\n")

        for i in range(0, 20):
            QuestionService.respond_to_question(5, author)
            print(Competency.objects.all().first().competency)
      

    def test_answering_multiple_questions(self):
        # New question with existing items with single topic
        # New question with existing items with multiple topics
        self.assertEqual(True, True)
