# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads

from django.http import JsonResponse
from users.services.UserService import logged_in_user, user_courses, update_course
from users.services.TokenService import token_valid, generate_token, token_to_user_course


def index(request):
    return JsonResponse({
        "login": "Returns a token to authenticate against the server"
    })


def me(request):
    token = request.META.get("HTTP_AUTHORIZATION", None)
    user_course = token_to_user_course(token)

    return JsonResponse(user_course.toJSON())


def courses(request):
    user = logged_in_user(request)
    return JsonResponse(user_courses(user), safe=False)


def update(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    user = logged_in_user(request)
    return JsonResponse(update_course(user, post_request), safe=False)


def login(request, course_code):
    token = request.META.get("HTTP_AUTHORIZATION", None)
    if token != "" and token is not None:
        if not token_valid(token):
            return JsonResponse({
                "token": token
            })
        user_course = token_to_user_course(token)
        return JsonResponse(generate_token(user=user_course.user, course_code=course_code), safe=False)

    return JsonResponse(generate_token())
