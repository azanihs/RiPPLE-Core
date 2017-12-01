# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from django.test import TestCase
from questions.models import Course, Topic, Question, Distractor
from users.models import User

class BootstrapTestCase(TestCase):
    def _bootstrap_courses(self, id):
        return Course.objects.create(course_code="test_course_" + str(id), course_name="course_name_" + str(id))


    def _bootstrap_topics(self, course):
        return [Topic.objects.create(name=x, course=course)
         for x in ["t1", "t2", "t3", "t4", "t5", "t6"]]

    def _bootstrap_questions(self, author, offset=0):
        # Allow offseting question/topic relations by a constant amount
        topic_map = [
            Topic.objects.filter(id__in=[offset + 1]),
            Topic.objects.filter(id__in=[offset + 1, offset + 2]),
            Topic.objects.filter(id__in=[offset + 2, offset + 3, offset + 4]),
            Topic.objects.filter(id__in=[offset + 4]),
            Topic.objects.filter(id__in=[offset + 2, offset + 4])
        ]

        #Modifier created to handle multiple users creating questions
        id_modifier = 5 * (author.user.id - 1) + 1

        for i in range(0, 5):
            q = Question(
                id=i + id_modifier,
                author=author,
                content="",
                explanation="",
                difficulty=0,
                quality=0,
                difficultyCount=0,
                qualityCount=0
            )
            q.save()
            q.topics.set(topic_map[i])

    def _bootstrap_questions_same_topics(self, author, topics):
        for i in range(5):
            q = Question(
                author=author,
                content="",
                explanation="",
                difficulty=0,
                quality=0,
                difficultyCount=0,
                qualityCount=0
            )
            q.save()
            q.topics.set(topics)

    def _bootstrap_question_choices(self, correct_id):
        #correct_id will specify the question correctly out of the distractors. Ex. 2 == option b is correct for all questions
        question_count = Question.objects.all().count()
        for i in range(0, (4 * question_count)):
            id = i + 1
            p_question_id = math.ceil(id / 4.0)
            Distractor(
                id=id,
                content="question " + str(i),
                response=chr(ord('A') + (id - 1) % 4),
                isCorrect=id == (correct_id + (p_question_id - 1) * 4),
                question_id=p_question_id
            ).save()

    def _bootstrap_user(self, id):
        user = User(id=id, first_name="u_firstname", last_name="u_lastname")
        user.save()
        return user
