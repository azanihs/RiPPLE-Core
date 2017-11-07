from ..models import Day, Time, Availability
from django.db.models import Count

def get_user_availability(course_user):
    return Availability.objects.filter(course_user=course_user)

def get_course_availability(course):
    return [x for x in Availability.objects.values('day', 'time').annotate(entries=Count('id')).order_by('day_id', 'time_id')]
