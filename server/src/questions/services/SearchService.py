from __future__ import unicode_literals
from questions.models import Question, QuestionResponse, Topic, Distractor
from users.models import CourseUser, Course
from django.db.models import Count, Subquery, OuterRef, Func, F


class SearchService(object):
    def __init__(self, course):
        super(SearchService, self).__init__()
        #Some questions occur multiple times due to some having multiple tags
        #Make distinct
        self._query = Question.objects.filter(
            author__in=CourseUser.objects.filter(course=course)).order_by("id").distinct()

    def add_sort(self, sort_field, sort_order):
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
            self._query = self._query.annotate(responses=Subquery(
                Distractor.objects.filter(question_id=OuterRef("pk"))
                .annotate(c=Count("questionresponse")).values("c").annotate(
                    s=Func(F("c"), function="LOWER")).values("c")))
            self._query = self._query.order_by(sort_modifier + sort_field)

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
        elif filter_field == "wrong":
            # All answered Questions where the Response has the isCorrect=True property
            self._query = self._query.filter(
                id__in=Distractor.objects.filter(
                    isCorrect=False,
                    id__in=QuestionResponse.objects.filter(
                        user=course_user).values("response_id")).values("question_id"))

    def text_search(self, text_query):
        self._query = self._query.filter(content__contains=text_query)
        # self._query = self._query.filter(topics__in=Topic.objects.filter(name__contains=text_query))

    def add_topic_filter(self, topics):
        self._query = self._query.filter(topics__in=topics)

    def execute(self):
        return self._query
