from ..models import Day, Time, Availability


def get_user_availability(course_user):
    return availabilities = Availability.objects.filter(course_user)
