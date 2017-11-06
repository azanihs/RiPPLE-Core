# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads

from django.http import JsonResponse, HttpResponse

from recommendations.services import AvailabilityService

def user_availability(request):
    logged_in_user = UserService.logged_in_user(request)
    availability = AvailabilityService.get_user_availability(logged_in_user)
    return JsonResponse(availability, safe=False)

def course_availability(request):
    logged_in_user = UserService.logged_in_user(request)
    # Get the count of each user in the course
    return None

def update(request):
    # HTTP.POST is required for this.
    return None
