# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads
import json
import base64
import imghdr
from django.http import JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from users.services import UserService
from users.services.TokenService import token_valid, generate_token, token_to_user_course, get_user
from users.models import User, Notification
from rippleAchievements.models import Achievement
from rippleAchievements.engine import engine
from ripple.util import util

def index(request):
    return JsonResponse({
        "data": {
            "login": "Returns a token to authenticate against the server"
        }
    })


def me(request):
    token = request.META.get("HTTP_AUTHORIZATION", None)
    user_course = token_to_user_course(token)

    return JsonResponse({"data": user_course.toJSON()})


def courses(request):
    user = UserService.logged_in_user(request)
    return JsonResponse({"data": UserService.user_courses(user)})


def update(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    post_request = loads(request.body.decode("utf-8"))
    user = UserService.logged_in_user(request)
    return JsonResponse({"data": UserService.update_course(user, post_request)})


def login(request, course_code):
    token = request.META.get("HTTP_AUTHORIZATION", None)
    if token != "" and token is not None:
        if not token_valid(token):
            return JsonResponse({
                "data": {
                    "token": token
                }
            })
        user_course = token_to_user_course(token)
        return JsonResponse({"data": generate_token(user=user_course.user, course_code=course_code)})

    return JsonResponse({"data": generate_token()})

def get_user(request, course_code=None):
    if course_code != "":
        return JsonResponse({"data": get_user(course_code)})

    return JsonResponse({"error": "Course not provided"})

def image_update(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)
    post_request = loads(request.body.decode("utf-8"))
    new_image = post_request.get("image", None)
    if new_image is None:
        return JsonResponse({
            "error": "Missing image payload"
        }, status=405)

    course_user = UserService.logged_in_user(request)

    root_path = util.generate_static_path(request.get_host())

    return JsonResponse(UserService.update_user_image(course_user.user, root_path, new_image))


def get_all_user_achievements(request):
    user = UserService.logged_in_user(request)

    achievements = Achievement.objects.all()
    data = []
    for ach in achievements:
        result = engine.check_achievement(user=user, key=ach.key)
        data.append(result)
        if result["new"]:
            n = Notification (
                name=result["name"] + " Earned",
                description=result["description"],
                icon=result["icon"],
                user=user
            )
            n.save()

    return JsonResponse({"data": data})

def get_all_notifications(request):
    user = UserService.logged_in_user(request)

    notifications = Notification.objects.filter(user=user).order_by("-id")
    data = []

    for n in notifications:
        n.sent = True
        data.append(n.toJSON())

    return JsonResponse({"data": data })

def engagement(request):
    user = UserService.logged_in_user(request)
    engagement_list = UserService.get_all_engagements(user)
    return JsonResponse({"data": engagement_list})

def engagement_all(request):
    user = UserService.logged_in_user(request)
    engagement = UserService.user_engagement(user)
    return JsonResponse({"data": engagement})

def engagement_aggregate(request, compare_type):
    user = UserService.logged_in_user(request)
    engagement = UserService.user_engagement(user, compare_type)
    return JsonResponse({"data": engagement})

def consent(request):
    user = UserService.logged_in_user(request)
    if request.method == 'POST':
        post_request = loads(request.body.decode("utf-8"))
        return JsonResponse(UserService.consent_service(user, post_request))
    else:
        return JsonResponse(UserService.get_user_consent(user))


def submit_consent_form(request):
    user = UserService.logged_in_user(request)
    post_request = loads(request.body.decode("utf-8"))
    return JsonResponse(UserService.update_consent_form(user, post_request, request.get_host()))

def consent_form(request):
    user = UserService.logged_in_user(request)
    return JsonResponse(UserService.get_consent_form(user))

def has_consented(request):
    user = UserService.logged_in_user(request)
    return JsonResponse(UserService.has_consented_course(user))

