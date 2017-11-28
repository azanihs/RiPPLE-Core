# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz as timezone

from django.conf import settings
from datetime import datetime
from ripple.util.util import save_image, mean

from questions.models import Topic, Competency
from questions.services import CompetencyService
from users.models import Course, CourseUser, User, Role, UserImage
from users.services.TokenService import token_to_user_course
from ripple.util import util

def update_user_image(user, server_root, new_image):
    saved_image = save_image(new_image, str(user.id))
    if saved_image is None:
        return {
            "error": "Image is not of valid type"
        }

    profile_image = UserImage.objects.create(
        image=saved_image,
        user=user
    )

    user.image = util.merge_url_parts([server_root, profile_image.image.name])
    user.save()
    return user.toJSON()


def logged_in_user(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is not None:
        return token_to_user_course(token)

    raise Exception("User not associated with token")


def user_courses(course_user):
    return [x.course.toJSON() for x in CourseUser.objects.filter(user=course_user.user)]


def update_course(course_user, new_data):
    course_information = new_data.get("course", {})
    topics = new_data.get("topics", None)
    if not topics:
        return {"error": "Course must have topics"}

    course_code = course_information.get("courseCode", None)
    if course_code is None:
        return {"error": "Missing course code"}

    if course_user.course.course_code != course_code:
        return {"error": "Course not found"}

    if "Instructor" not in (x.role for x in course_user.roles.all()):
        return {"error": "User does not have administrative permission for current context"}

    start = course_information.get("start", None)
    end = course_information.get("end", None)
    available = course_information.get("available", None)

    course = course_user.course
    if available is not None:
        course.available = available
    if start is not None:
        if str(start).isdigit():
            course.start = datetime.fromtimestamp(int(start), timezone.utc)
        else:
            return {"error": "Given start timestamp is not valid: " + start}
    if end is not None:
        if str(end).isdigit():
            course.end = datetime.fromtimestamp(int(end), timezone.utc)
        else:
            return {"error": "Given end timestamp is not valid: " + end}

    course.save()
    original_topics = course.topic_set.all()
    new_topics = []
    # Insert topics
    for topic in topics:
        topic_id = topic.get("id", None)
        topic_name = topic.get("name", None)
        if topic_id is None:
            new_topics.append(Topic.objects.create(
                name=topic_name, course=course))
        elif topic_id is not None:
            try:
                existing_topic = Topic.objects.get(pk=topic_id)
                existing_topic.name = topic_name
                existing_topic.course = course
                existing_topic.save()
                new_topics.append(existing_topic)
            except Topic.DoesNotExist:
                pass

    def exists_by_id(topic_list, id):
        for t in topic_list:
            if t.id == id:
                return True
        return False
    # Trim out old topics
    for i in original_topics:
        if exists_by_id(new_topics, i.id) is False:
            i.delete()

    return course_user.toJSON()


def get_course_by_id(course_code):
    try:
        course = Course.objects.get(course_code=course_code)
        return course.toJSON()
    except Course.DoesNotExist:
        return {
            "error": "Course not available"
        }
def group_competencies(competencies):
    def _group_competencies(carry, c):
        if carry.get(c.topics, None) is None:
            carry[c.topics] = []

        carry[c.topics].append(c)
        return carry

    group = {}
    for i in competencies:
        group = _group_competencies(group, i)
    return group

def _process_competencies(competencies):

    edges = []
    threshold = settings.RUNTIME_CONFIGURATION["min_competency_threshold"]

    for topic_group, competency_group in group_competencies(competencies).items():
        competency = mean([x.competency for x in competency_group])
        confidence = 0
        if competency < threshold:
            continue

        nodes = CompetencyMap.objects.filter(aggregate_id=topic_group)
        source = nodes.first()
        target = nodes.last()

        edges.append([
            source.topic.toJSON(),
            target.topic.toJSON(),
            competency,
            confidence
        ])

    return edges

def user_competencies(user):
    return _process_competencies(Competency.objects.filter(user=user))

def aggregate_competencies(user, compare_type):
    if compare_type == "peer":
        competencies = Competency.objects.filter(user__in=CourseUser.objects.filter(course=user.course))
    else:
        # TODO: handle other compare_types
        competencies = Competency.objects.filter(user__in=CourseUser.objects.filter(course=user.course))

    return _process_competencies(competencies)

def insert_course_if_not_exists(course):
    try:
        return Course.objects.get(course_code=course.get("course_code"))
    except Course.DoesNotExist:
        return Course.objects.create(course_code=course.get("course_code"), course_name=course.get("course_name"))


def insert_user_if_not_exists(user):
    try:
        return User.objects.get(user_id=user.get("user_id"))
    except User.DoesNotExist:
        return User.objects.create(user_id=user.get("user_id"), first_name=user.get("first_name"), last_name=user.get("last_name"), image="")


def insert_course_user_if_not_exists(course, user):
    try:
        return CourseUser.objects.get(course=course, user=user)
    except CourseUser.DoesNotExist:
        return CourseUser.objects.create(course=course, user=user)


def update_user_roles(course_user, role):
    # Insert role if not exists
    try:
        saved_role = Role.objects.get(role=role)
    except Role.DoesNotExist:
        saved_role = Role.objects.create(role=role)

    if saved_role not in course_user.roles.all():
        course_user.roles.add(saved_role)
