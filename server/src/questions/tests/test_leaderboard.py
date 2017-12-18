# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questions.services import QuestionService
from users.models import CourseUser

from .common import BootstrapTestCase

class LeaderboardTest(BootstrapTestCase):
    def _boostrap_leaderboard_users(self, course, user_id, make_questions=False):
        user = self._bootstrap_user(user_id)
        author = CourseUser.objects.create(user=user, course=course)
        if make_questions:
            self._bootstrap_questions(author)

    def test_leaderboard_fetch(self):
        """ Tests fetching leaderboard results"""
        course = self._bootstrap_courses(1)
        course_user = self._bootstrap_course_user(-1, course)
        self._bootstrap_topics(course)
        for i in [1,2,3,4,5]:
            self._boostrap_leaderboard_users(course, i, i == 1)

        leaderboard = QuestionService.get_course_leaders(course, "questionsAuthored", "", course_user)
        self.assertEqual(len(leaderboard), 5+1) # +1 for current user

    def test_leaderboard_sort_direction(self):
        course = self._bootstrap_courses(1)
        course_user = self._bootstrap_course_user(-1, course)
        self._bootstrap_topics(course)
        for i in [1,2,3,4,5]:
            self._boostrap_leaderboard_users(course, i, i == 1)

        leaderboard = QuestionService.get_course_leaders(course, "questionsAuthored", "DESC", course_user)
        self.assertEqual(len(leaderboard), 5+1) # +1 for current user
        self.assertEqual(leaderboard[0]["questionsAuthored"], 5)
        self.assertEqual(leaderboard[1]["questionsAuthored"], 0)

        # Sort in other direction
        leaderboard = QuestionService.get_course_leaders(course, "questionsAuthored", "ASC", course_user)
        self.assertEqual(len(leaderboard), 5+1) # +1 for current user
        self.assertEqual(leaderboard[0]["questionsAuthored"], 0)
        self.assertEqual(leaderboard[-1]["questionsAuthored"], 5)

    def test_leaderboard_fetch_multiple(self):
        """ Tests fetching leaderboard results with multiple courses"""
        courses = [self._bootstrap_courses(1), self._bootstrap_courses(2)]
        course_user = self._bootstrap_course_user(-1, courses[0])
        course_user_2 = self._bootstrap_course_user(-2, courses[1])
        for count, course in enumerate(courses):
            self._bootstrap_topics(course)
            for i in range((count+1) * 5):
                id = i + count*5
                self._boostrap_leaderboard_users(course, id, id == count)

        leaderboard = QuestionService.get_course_leaders(courses[0], "questionsAuthored", "", course_user)
        self.assertEqual(len(leaderboard), 5+1) # +1 for current user

        leaderboard = QuestionService.get_course_leaders(courses[1], "questionsAuthored", "", course_user_2)
        self.assertEqual(len(leaderboard), 10+1) # +1 for current user

    def test_leaderboard_fetch_many(self):
        """ Tests limiting of leaderboard fetching results"""
        course = self._bootstrap_courses(1)
        course_user = self._bootstrap_course_user(-1, course)
        self._bootstrap_topics(course)
        for i in range(0, 100):
            self._boostrap_leaderboard_users(course, i, i == 1)

        leaderboard = QuestionService.get_course_leaders(course, "questionsAuthored", "DESC", course_user)
        self.assertEqual(len(leaderboard), 25)

    def test_leaderboard_fetch_many_instructor(self):
        """ Tests limiting of leaderboard fetching results for instructor"""
        course = self._bootstrap_courses(1)
        course_user = self._bootstrap_course_user(-1, course)
        self._bootstrap_topics(course)
        for i in range(0, 100):
            self._boostrap_leaderboard_users(course, i, i == 1)
        leaderboard = QuestionService.get_course_leaders(course, "questionsAuthored", "DESC", course_user, limit=-1)
        self.assertEqual(len(leaderboard), 100+1) #current user
