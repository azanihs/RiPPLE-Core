from ..models import Day, Time, Availability


def get_user_availability(course_user):
    availability = Availability.objects.filter(course_user=course_user)
    return availability
