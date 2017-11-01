from django.http import JsonResponse
from users.services.TokenService import token_valid
from django.conf import settings


class TokenValidator(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        prefix = settings.FORCE_SCRIPT_NAME

        def pre(x):
            return request.path == (prefix + x)

        using_lti_login = pre('/lti') or pre('/lti/')
        if using_lti_login:
            return self.get_response(request)

        # LTI is the only allowed endpoint without a token
        if token is None and not settings.ALLOW_UNAUTHENTICATED:
            return JsonResponse({
                "error": "Missing token in Authorization header."
            }, status=401)

        return self.get_response(request)
