# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads
from users.models import CourseUser

from django.http import JsonResponse, HttpResponse

from users.services import UserService
from recommendations.services import AvailabilityService

def user_availability(request):
    logged_in_user = UserService.logged_in_user(request)
    availability = [x.toJSON() for x in AvailabilityService.get_user_availability(logged_in_user)]
    return JsonResponse(availability, safe=False)

def course_availability(request):
    course = UserService.logged_in_user(request).course
    counts = AvailabilityService.get_course_availability(course)

    # Get the count of each user in the course
    return JsonResponse(counts, safe=False)

def update(request):
    # HTTP.POST is required for this.
    if request.method != "POST":
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    logged_in_user = UserService.logged_in_user(request)

    post_request = loads(request.body.decode("utf-8"))
    day = post_request.get("day", None)
    time = post_request.get("time", None)

    if AvailabilityService.update_availability(logged_in_user, day, time) is None:
        return JsonResponse({"error": "Invalid day/time/availability combination"}, status=422)
    else:
        return HttpResponse(status=204)

def utc_times(request):
    times = [x.toJSON() for x in AvailabilityService.get_utc_times()]
    return JsonResponse(times, safe=False)

def study_roles(request):
    roles = [x.toJSON() for x in AvailabilityService.get_study_roles()]
    return JsonResponse(roles, safe=False)

def user_roles(request):
    logged_in_user = UserService.logged_in_user(request)
    available_roles = [x.toJSON() for x in AvailabilityService.get_user_available_roles(logged_in_user)]
    return JsonResponse(available_roles, safe=False)
