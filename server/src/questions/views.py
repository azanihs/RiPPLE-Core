# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads

from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from ripple.util.util import is_number, merge_url_parts
from users.services import UserService
from questions.services import QuestionService, SearchService, AuthorService


def add(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    def _format(x):
        if len(x) == 0: return x
        return (x + "/") if x[-1] != "/" else x
    root_path = merge_url_parts([
        _format("//" + request.get_host()),
        _format(settings.FORCE_SCRIPT_NAME),
        _format("static")
    ])

    post_request = loads(request.body.decode("utf-8"))

    if post_request is None:
        return JsonResponse({"error": "Missing question in request"}, status=422)

    response = AuthorService.add_question(
        post_request, root_path, UserService.logged_in_user(request))

    if response['state'] == "Error":
        return JsonResponse({"error": response['error']}, status=422)
    else:
        return JsonResponse({
            "data": {
                "question": response['question']
            }
        })


def respond(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    distractor_id = post_request.get("distractorID", None)

    try:
        if distractor_id is None:
            return JsonResponse({"error": "Missing integer distractorID in request"}, status=422)
        if QuestionService.respond_to_question(distractor_id, UserService.logged_in_user(request)) is False:
            return JsonResponse({"error": "Invalid distractorID"}, status=422)
        else:
            return JsonResponse({})
    except ValueError:
        return JsonResponse({"error": "You are not enrolled in the course for this course"}, status=403)

def rate(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    distractor_id = post_request.get("distractorID", None)

    difficulty = post_request.get("difficulty", None)
    quality = post_request.get("quality", None)

    if difficulty is None and quality is None:
        return JsonResponse({"error": "At least response.rating or response.quality must be specified"}, status=422)

    if difficulty is not None:
        if is_number(difficulty) is False or not 0 <= int(difficulty) <= 5:
            return JsonResponse({"error": "response.difficulty must be between 0 and 5 inclusive"}, status=422)
        difficulty = int(difficulty)

    if quality is not None:
        if is_number(quality) is False or not 0 <= int(quality) <= 5:
            return JsonResponse({"error": "response.quality must be between 0 and 5 inclusive"}, status=422)
        quality = int(quality)

    if distractor_id is None:
        return JsonResponse({"error": "Missing integer distractorID in request"}, status=422)

    user_ratings = {"difficulty": difficulty, "quality": quality}
    if QuestionService.rate_question(distractor_id, user_ratings, UserService.logged_in_user(request)) is False:
        return JsonResponse({"error": "Invalid distractorID"}, status=422)
    else:
        return HttpResponse(status=204)


def index(request):
    return JsonResponse({
        "all": "Returns all Questions",
        "topics": "Returns all Question Topics",
        "id/:id": "Fetch question by ID",
        "search/sortField/:sortField/sortOrder/:sortOrder/filterField/:filterField/query/:query": "Run a server search",
        "page/:id": "Fetch question collection in chunks",
        "competencies/all": "Fetch all competencies for the user",
        "add": "Add a question to the database",
        "report": "Report a question",
    })


def random_question_id(request):
    logged_in_user = UserService.logged_in_user(request)
    question = QuestionService.get_random_question(logged_in_user)
    if question is None:
        return JsonResponse({"error": "You are not enrolled in the course for this question"}, status=403)

    return JsonResponse({"data": question.id})

def id(request, id):
    logged_in_user = UserService.logged_in_user(request)
    question = QuestionService.get_question_by_id(logged_in_user, id)

    if question is None:
        return JsonResponse({"error": "You are not enrolled in the course for this question"}, status=403)

    return JsonResponse({"data": question.toJSON()})


def competencies(request):
    logged_in_user = UserService.logged_in_user(request)
    user_competencies = UserService.user_competencies(logged_in_user)
    return JsonResponse({"data": user_competencies})

def aggregate(request, compare_type):
    logged_in_user = UserService.logged_in_user(request)
    aggregate_competencies = UserService.aggregate_competencies(logged_in_user, compare_type)
    return JsonResponse({"data": aggregate_competencies})

def distribution(request, question_id):
    question_distribution = QuestionService.question_response_distribution(question_id)
    return JsonResponse({"data": question_distribution})

def leaderboard_default(request):
    return leaderboard(request, "reputation", "DESC")


def leaderboard(request, sort_field, sort_order):
    logged_in_user = UserService.logged_in_user(request)
    user_roles = (str(x) for x in logged_in_user.roles.all())
    limit = -1 if "Instructor" in user_roles else 20

    if sort_order != "DESC" and sort_order != "ASC":
        sort_order = "ASC"

    leaderboard_scores = QuestionService.get_course_leaders(
        logged_in_user.course, sort_field, sort_order, limit)
    return JsonResponse({"data": leaderboard_scores})


def topics(request):
    logged_in_user = UserService.logged_in_user(request)
    course_topics = QuestionService.get_course_topics(logged_in_user.course)
    unique_topics = [x.toJSON() for x in course_topics]

    return JsonResponse({"data": unique_topics})


def search(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    logged_in_user = UserService.logged_in_user(request)
    search_query = SearchService.SearchService(logged_in_user.course)
    post_request = loads(request.body.decode("utf-8"))
    sort_field = post_request.get("sortField", None)
    filter_field = post_request.get("filterField", None)
    filter_topics = post_request.get("filterTopics", None)
    query = post_request.get("query", None)
    sort_order = post_request.get("sortOrder", None)
    page_index = post_request.get("page", None)
    page_size = post_request.get("pageSize", 25)

    if sort_field is None and filter_field is None and query is None:
        search_result = search_query.execute()
        return page_response(search_result, page_index, page_size)

    if sort_field is not None:
        search_query.add_sort(sort_field, sort_order)

    if filter_field is not None:
        search_query.add_filter(filter_field, logged_in_user)

    if filter_topics is not None:
        search_query.add_topic_filter(filter_topics)

    if query is not None:
        search_query.text_search(query)

    try:
        search_result = search_query.execute()
        return page_response(search_result, page_index, page_size)
    except TypeError as e:
        return JsonResponse({
            "error": e
        })

def page_response(data, page_index, page_size=25):
    page_manager = Paginator(data, page_size)
    try:
        page = page_manager.page(page_index)
    except PageNotAnInteger:
        page_index = 1
        page = page_manager.page(page_index)
    except EmptyPage:
        page_index = page_manager.num_pages
        page = page_manager.page(page_index)

    return JsonResponse({
        "data": {
            "items": [x.toJSON() for x in page.object_list],
            "page": page_index,
            "totalItems": page_manager.count
        }
    })

def report(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    user = UserService.logged_in_user(request)
    return JsonResponse({"data": QuestionService.report_question(user, post_request)})

def all_reports(request):
    user = UserService.logged_in_user(request)

    result = QuestionService.all_reports(user)
    if type(result) != list and result.get("error", None) is not None:
        return JsonResponse(result)
    else:
        return JsonResponse({"data": result})


def get_reasons(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    user = UserService.logged_in_user(request)
    return JsonResponse({"data": QuestionService.get_reason_list(user)})
