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

def days(request):
    days = [x.toJSON() for x in AvailabilityService.get_days()]
    return JsonResponse(days, safe=False)

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
    updated_availability = AvailabilityService.update_availability(logged_in_user, day, time)
    if updated_availability is None:
        return JsonResponse({"error": "Invalid day/time/availability combination"}, status=422)
    else:
        return JsonResponse(updated_availability.toJSON())

def utc_times(request):
    times = [x.toJSON() for x in  AvailabilityService.get_utc_times()]
    return JsonResponse(times, safe=False)
