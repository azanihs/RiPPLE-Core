from ..models import Day, Time, Availability, StudyRole, Request
from questions.models import Topic

from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

def get_user_availability(course_user):
    return Availability.objects.filter(course_user=course_user)

def get_course_availability(course):
    return [x for x in Availability.objects.filter(course_user__course=course).values('day', 'time').annotate(entries=Count('id')).order_by('day_id', 'time_id')]

def get_days():
    return Day.objects.all()

def get_utc_times():
    return Time.objects.all()

def update_availability(course_user, day_id, time_id):
    # Check if availaibility exists
    try:
        availability = Availability.objects.get(course_user=course_user, day=day_id, time=time_id)
        availability.delete()
        return availability
    except Availability.DoesNotExist:
        try:
            day = Day.objects.get(pk=day_id)
        except Time.DoesNotExist:
            return None
        try:
            time = Time.objects.get(pk=time_id)
        except Time.DoesNotExist:
            return None
        availability = Availability(course_user=course_user, day=day, time=time)
        availability.save()
        return availability

def get_study_roles():
    return StudyRole.objects.all()

def get_user_available_roles(course_user):
    return Request.objects.filter(course_user=course_user)

def update_role(course_user, topic_id, study_role_id):
    # Check if availaibility exists
    try:
        available_role = Request.objects.get(course_user=course_user, topic=topic_id, study_role=study_role_id)
        exists = True
    except ObjectDoesNotExist:
        exists = False

    if exists:
        available_role.delete()
        return available_role

    else:
        try:
            topic = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            return None
        try:
            study_role = StudyRole.objects.get(pk=study_role_id)
        except ObjectDoesNotExist:
            return None
        available_role = Request(course_user=course_user, topic=topic, study_role=study_role)
        available_role.save()
        return available_role
