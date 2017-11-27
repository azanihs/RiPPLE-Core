from ..models import Day, Time, Availability, StudyRole, AvailableRole
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


def get_user_availability(course_user):
    return Availability.objects.filter(course_user=course_user)

def get_course_availability(course):
    return [x for x in Availability.objects.values('day', 'time').annotate(entries=Count('id')).order_by('day_id', 'time_id')]

def get_utc_times():
    return Time.objects.all()

def update_availability(course_user, day_id, time_id):
    # Check if availaibility exists
    try:
        availability = Availability.objects.get(course_user=course_user, day=day_id, time=time_id)
        exists = True
    except ObjectDoesNotExist:
        exists = False

    if exists:
        availability.delete()
        return True

    if not exists:
        day = Day.objects.get(pk=day_id)
        time = Time.objects.get(pk=time_id)
        availability = Availability(course_user=course_user, day=day, time=time)
        availability.save()
        return True

    return None

def get_study_roles():
    return StudyRole.objects.all()

def get_user_available_roles(course_user):
    return AvailableRole.objects.filter(course_user=course_user)
