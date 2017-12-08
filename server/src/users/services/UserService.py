# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz as timezone

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.apps import apps
from datetime import datetime
from ripple.util.util import save_image, mean

from questions.models import Topic, Competency, Distractor, QuestionResponse, Question, QuestionRating
from questions.services import CompetencyService
from users.models import Course, CourseUser, User, Role, UserImage, Engagement
from rippleAchievements.models import UserAchievement
from users.services.TokenService import token_to_user_course
from ripple.util import util

competency_threshold = settings.RUNTIME_CONFIGURATION["min_competency_value"]

def update_user_image(user, server_root, new_image):
    if new_image is None:
        return {
            "error": "No image provided"
        }
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
    if request is None or not request:
        return {"error": "Request must be provided"}
    token = request.META.get("HTTP_AUTHORIZATION", None)
    if token is not None:
        return token_to_user_course(token)

    raise Exception("User not associated with token")


def user_courses(course_user):
    if course_user is None or not course_user:
        return {"error": "CourseUser must be provided"}
    return [x.course.toJSON() for x in CourseUser.objects.filter(user=course_user.user)]


def update_course(course_user, new_data):
    if course_user is None or new_data is None \
            or not course_user or not new_data:
        return {"error": "Course user and update data must be provided"}
    course_information = new_data.get("course", {})
    topics = new_data.get("topics", None)
    if not topics:
        return {"error": "Course must have topics"}
    for t in topics:
        if not t.get("name", None):
            return {"error":
                "Topics must be JSON representations of Topics with, at minimum, attribute 'name'"}

    course_code = course_information.get("courseCode", None)
    if course_code is None:
        return {"error": "Missing course code"}

    if course_user.course.course_code != course_code:
        return {"error": "Course not found"}

    if not util.is_administrator(course_user):
        return {"error": "User does not have administrative permission for current context"}

    start = course_information.get("start", None)
    end = course_information.get("end", None)
    available = course_information.get("available", None)

    course = course_user.course
    if start is not None:
        if str(start).isdigit():
            course.start = datetime.fromtimestamp(int(start), timezone.utc)
        else:
            return {"error": "Given start timestamp is not valid: " + str(start)}
    if end is not None:
        if str(end).isdigit():
            course.end = datetime.fromtimestamp(int(end), timezone.utc)
        else:
            return {"error": "Given end timestamp is not valid: " + str(end)}

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
            if not str(topic_id).isdigit():
                return {"error": "Invalid Topic ID"}
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

def _process_competencies(competencies):
    if competencies is None:
        return []
    edges = []
    threshold = settings.RUNTIME_CONFIGURATION["min_competency_threshold"]
    for comp in competencies:
        if comp.confidence < threshold:
            continue

        # Only use two topics.
        nodes = comp.topics.all()
        if not(len(nodes) > 0 and len(nodes) <= 2):
            continue

        source = nodes.first()
        target = nodes.last()
        edges.append([
            source.toJSON(),
            target.toJSON(),
            comp.competency,
            comp.confidence
        ])
    return edges

def user_competencies(user):
    try:
        return _process_competencies(Competency.objects.filter(user=user))
    except TypeError:
        return[]

def aggregate_competencies(user, compare_type):
    if user is None or compare_type is None:
        return []
    if compare_type == "peers":
        competencies = Competency.objects.filter(user__in=CourseUser.objects.filter(course=user.course))
    else:
        # TODO: handle other compare_types
        competencies = Competency.objects.filter(user__in=CourseUser.objects.filter(course=user.course))

    return _process_competencies(competencies)

def insert_course_if_not_exists(course):
    if course is None or course.get("course_name", None) is None \
            or course.get("course_code", None) is None:
        return {"error": "Invalid Course Provided"}
    try:
        return Course.objects.get(course_code=course.get("course_code"))
    except Course.DoesNotExist:
        return Course.objects.create(course_code=course.get("course_code"), course_name=course.get("course_name"))


def insert_user_if_not_exists(user):
    if user is None or user.get("user_id", None) is None:
        return {"error": "Invalid User Provided"}
    try:
        return User.objects.get(user_id=user.get("user_id"))
    except User.DoesNotExist:
        if user.get("first_name", None) is None or user.get("last_name", None) is None \
                or user.get("image", None) is None:
            return {"error": "Invalid User Provided"}
        return User.objects.create(user_id=user.get("user_id"), first_name=user.get("first_name"), last_name=user.get("last_name"), image="")


def insert_course_user_if_not_exists(course, user):
    if course is None or not isinstance(course, Course):
        return {"error": "Invalid Course Provided"}
    if user is None or not isinstance(user, User):
        return {"error": "Invalid User Provided"}
    try:
        return CourseUser.objects.get(course=course, user=user)
    except CourseUser.DoesNotExist:
        return CourseUser.objects.create(course=course, user=user)


def update_user_roles(course_user, role):
    if course_user is None or not isinstance(course_user, CourseUser):
        return {"error": "Invalid CourseUser Provided"}
    if role is None:
        return {"error": "Invalid Role Provided"}
    # Insert role if not exists
    try:
        saved_role = Role.objects.get(role=role)
    except Role.DoesNotExist:
        saved_role = Role.objects.create(role=role)

    if saved_role not in course_user.roles.all():
        course_user.roles.add(saved_role)

def get_all_engagements(user):
    course = user.course
    engagements = Engagement.objects.filter(course=course)
    engagements = [x.toJSON() for x in engagements]
    for e in engagements:
        e["id"] = -e["id"]
    return engagements

def user_engagement(user, user_type=None):
    edges = []
    engagements = Engagement.objects.filter(course=user.course)

    #Compare against self
    if not user_type:
        user_type=user

    #Filters
    filters = {
        "isCorrect": ["response_id__in", Distractor.objects.filter(isCorrect=True)]
    }

    for e in engagements:
        model = ContentType.objects.get(model=e.model).model_class()
        e_filter = filters.get(e.filter_name, None)
        if e_filter:
            filter_name = e_filter[0]
            filter_cond = e_filter[1]
        else:
            filter_name = None
            filter_cond = None
        key_user = e.key_user
        edges.append([
            e.toJSON(),
            e.toJSON(),
            get_engagement_result(user_type, model, filter_name, filter_cond, key_user),
            0
        ])
    return edges

def get_engagement_result(user, model, filter_name, filter_cond, key_user):
    if filter_name:
        correct = model.objects.filter(**{filter_name:filter_cond})
    else:
        correct = model.objects.all()
    max_num = correct.values(key_user).annotate(num_results=Count(key_user))\
            .values("num_results").order_by("-num_results")
    if not max_num:
        return 0
    max_num = max_num[0]["num_results"]
    if user == "peers":
        num_users = correct.values(key_user).distinct().count()
        avg_correct = correct.count()/num_users
        return avg_correct/max_num
    else:
        user_correct = correct.filter(**{key_user:user}).count()
        return user_correct/max_num