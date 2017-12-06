from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings

from lti.services.LTIService import validate_lti_request, request_to_course, request_to_user, create_course_user
from users.services.TokenService import generate_token


def index(request):
    lti_params = request.POST
    lti_validation = validate_lti_request(
        request.build_absolute_uri(), request.method, lti_params)

    if lti_validation.get("error", None) is not None:
        user_response = {
            "error": lti_validation.get("error")
        }
        return JsonResponse(user_response)
    else:
        course = request_to_course(lti_params)
        user = request_to_user(lti_params)
        course_user = create_course_user(course, user, lti_params)

        # Get token
        token = generate_token(user, course.course_code)
        # Redirect to application
        url = settings.LTI["REDIRECT_URL"] + \
            "/#/?token=" + token.get("token") + \
            "&course_code=" + course.course_code

        return redirect(url)
