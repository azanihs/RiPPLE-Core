# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads

from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ripple.util.util import is_number
from users.services import UserService
from questions.services import QuestionService, SearchService


def respond(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    distractor_id = post_request.get("distractorID", None)

    if distractor_id is None:
        return JsonResponse({"error": "Missing integer distractorID in request"}, status=422)
    if QuestionService.respond_to_question(distractor_id, UserService.logged_in_user(request)) is None:
        return JsonResponse({"error": "Invalid distractorID"}, status=422)
    else:
        return HttpResponse(status=204)


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
    if QuestionService.rate_question(distractor_id, user_ratings, UserService.logged_in_user(request)) is None:
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
        "competencies/all": "Fetch all competencies for the user"
    })


def id(request, id):
    question = QuestionService.get_questions(id)

    if question is None:
        return JsonResponse({}, status=404)

    return JsonResponse(question.toJSON())


def competencies(request):
    logged_in_user = UserService.logged_in_user(request)
    user_competencies = UserService.user_competencies(logged_in_user)
    return JsonResponse(user_competencies, safe=False)


def all(request):
    logged_in_user = UserService.logged_in_user(request)
    all_questions = [x.toJSON()
                     for x in QuestionService.get_all_questions(logged_in_user.course)]
    return JsonResponse(all_questions, safe=False)


def topics(request):
    logged_in_user = UserService.logged_in_user(request)
    course_topics = QuestionService.get_course_topics(logged_in_user.course)
    unique_topics = [x.toJSON() for x in course_topics]

    return JsonResponse(unique_topics, safe=False)


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
    page = post_request.get("page", None)

    if sort_field is None and filter_field is None and query is None:
        found_questions = QuestionService.all_questions()
        return page_response(found_questions, page)

    if sort_field is not None:
        search_query.add_sort(sort_field, sort_order)

    if filter_field is not None:
        search_query.add_filter(filter_field)

    if filter_topics is not None:
        search_query.add_topic_filter(filter_topics)

    if query is not None:
        search_query.text_search(query)

    try:
        search_result = search_query.execute()
        return page_response(search_result, page)
    except TypeError:
        all_questions = QuestionService.all_questions()
        return page_response(all_questions, page)


def page(request, page):
    return page_response(QuestionService.all_questions(), page)


def page_response(data, page_index):
    page_manager = Paginator(data, 25)
    try:
        page = page_manager.page(page_index)
    except PageNotAnInteger:
        page_index = 1
        page = page_manager.page(page_index)
    except EmptyPage:
        page_index = page_manager.num_pages
        page = page_manager.page(page_index)

    return JsonResponse({
        "items": [x.toJSON() for x in page.object_list],
        "page": page_index,
        "totalItems": page_manager.count
    })