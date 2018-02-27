# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db import transaction
from users.models import Course, CourseUser, Token


def token_valid(token):
    if token is None:
        return False
    try:
        return Token.objects.get(payload=token) is not None
    except Token.DoesNotExist:
        return False


def make_token_string():
    digits = '1234567890'
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    token = ''.join(random.SystemRandom().choice(letters + digits)
                    for _ in range(32))
    if token_valid(token) is False:
        return token
    return make_token_string()


@transaction.atomic
def generate_token(user=None, course_id=None):
    if course_id is None and user is None:
        # Get random user to requester
        course_user = get_random_user()
    else:
        # User has access to course
        try:
            course_user = CourseUser.objects.get(
                user=user, course=Course.objects.get(course_id=course_id))
        except CourseUser.DoesNotExist:
            # User does not have access to it
            return ""

    return make_token(course_user)

@transaction.atomic
def generate_admin_token():
    course_user = get_admin_user()
    return make_token(course_user)

def make_token(course_user):
    token = make_token_string()
    new_token = Token(payload=token, user=course_user)
    new_token.save()

    return {
        "token": new_token.payload,
        "courseID": new_token.user.course.course_id
    }

def get_random_user():
    count = CourseUser.objects.count()
    random_index = random.randint(0, count - 1)
    return CourseUser.objects.all()[random_index]

def get_admin_user():
    count = CourseUser.objects.filter(roles__in=['Instructor', 'TeachingAssistant']).count()
    random_index = random.randint(0, count-1)
    return CourseUser.objects.all()[random_index]

def token_to_user_course(token):
    return Token.objects.get(payload=token).user


def get_user(course_id):
    if (Course.objects.filter(course_id=course_id).count() > 0):
        course_id = Course.objects.get(course_id=course_id).pk
    else:
        return {"error": "Course does not exist"}
    count = CourseUser.objects.filter(course_id=course_id).count()
    random_index = random.randint(0, count - 1)
    course_user = CourseUser.objects.filter(course_id=Course.objects.get(course_id=course_id))[random_index]
    
    token = make_token_string()
    new_token = Token(payload=token, user=course_user)
    new_token.save()

    return {
        "token": new_token.payload,
        "courseID": new_token.user.course.course_id
    }
