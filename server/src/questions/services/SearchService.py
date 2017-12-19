from __future__ import unicode_literals
from questions.models import Question, QuestionResponse, Topic, Distractor, QuestionScore
from users.models import CourseUser, Course
from django.db.models import Count, Subquery, OuterRef, Func, F


class SearchService(object):
    def __init__(self, course):
        super(SearchService, self).__init__()
        #Some questions occur multiple times due to some having multiple tags
        #Make distinct
        self._query = Question.objects.filter(
            author__in=CourseUser.objects.filter(course=course))

        # Default object order is by ID. Can possibly be overridden by search
        self._query = self._query.order_by("id")

    def add_sort(self, sort_field, sort_order, user):
        if sort_order == "DESC":
            sort_modifier = "-"
        else:
            sort_modifier = ""

        if sort_field in ["difficulty", "quality", "created_time"]:
            self._query = self._query.order_by(sort_modifier + sort_field)
        elif sort_field == "comments":
            pass
        elif sort_field == "personalisation":
            pass
            # Go somewhere else...
        elif sort_field == "responses":
            self._query = self._query.annotate(responses=\
                Count("distractor__questionresponse__user", distinct=True))
            self._query = self._query.order_by(sort_modifier + sort_field)
        elif sort_field == "recommended":
            user_rating = user.elo_rating
            self._query = self._query.annotate(difficulty_diff=0-Func(user_rating - F("elo_difficulty"), function="ABS"))
            self._query = self._query.order_by(sort_modifier + "difficulty_diff")

    def add_filter(self, filter_field, course_user):
        if filter_field == "unanswered":
            # All questions where the Question is NOT IN the Distractor Responses
            self._query = self._query.exclude(
                id__in=Distractor.objects.filter(
                    id__in=QuestionResponse.objects.filter(
                        user=course_user).values("response_id")).values("question_id"))

        elif filter_field == "answered":
            # All questions where the Question IS IN the Distractor Responses
            self._query = self._query.filter(
                id__in=Distractor.objects.filter(
                    id__in=QuestionResponse.objects.filter(
                        user=course_user).values("response_id")).values("question_id"))
        elif filter_field == "improve":
            # All answered Questions where the Response has the isCorrect=False property
            self._query = self._query.filter(
                id__in=Distractor.objects.filter(
                    id__in=QuestionResponse.objects.filter(
                        user=course_user).values("response_id")).values("question_id"))

            self._query = self._query.filter(id__in = QuestionScore.objects.filter(score__lt = 1))

    def text_search(self, text_query):
        self._query = self._query.filter(content__contains=text_query)
        # self._query = self._query.filter(topics__in=Topic.objects.filter(name__contains=text_query))

    def add_topic_filter(self, topics):
        self._query = self._query.filter(topics__in=topics)

    def execute(self):
        return self._query.distinct()
