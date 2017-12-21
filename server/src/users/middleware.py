from django.http import JsonResponse
from users.services.TokenService import token_valid, token_to_user_course
from django.conf import settings
from users.models import User
from rippleAchievements.models import View, Task, Achievement
from rippleAchievements.engine import engine
from users.models import Notification
import json


class TokenValidator(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)

        def pre(x):
            return request.path == x

        # If entering at the root, don't require auth header
        using_lti_login = pre('') or pre('/')
        if using_lti_login:
            return self.get_response(request)

        # LTI is the only allowed endpoint without a token
        if token is None and not settings.ALLOW_UNAUTHENTICATED:
            return JsonResponse({
                "error": "Missing token in Authorization header."
            }, status=401)

        return self.get_response(request)

class NotificationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        response = self.get_response(request)

        if token is None:
            return response
        try:
            user = token_to_user_course(token)
            data = json.loads(response.content.decode('utf-8'))
            notifications = Notification.objects.filter(user=user, sent=False)

            data["notifications"] = []
            for i in notifications:
                data["notifications"].append(i.toJSON())
                i.sent = True
                i.save()

            response.content = json.dumps(data)
        # Catch JSON decode error
        except ValueError:
            pass

        return response

class AchievementChecker(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.views = View.objects.all()

    def __call__(self, request):
        ###################
        # On client request
        ###################
        token = request.META.get("HTTP_AUTHORIZATION", None)

        def pre(x):
            return request.path == x or request.path == (x + "/")

        req = None
        # Identify which view the request is associated with if ach attached.
        for v in self.views:
            if pre(v.url):
                req = v.view

        if req is not None:
            req = View.objects.get(view=req)
            tasks = Task.objects.filter(views = req)

        response=self.get_response(request)

        ####################
        # On server response
        ####################
        if token is None or response.content is None or req is None:
            return response
        #data = json.loads(response.content.decode('utf-8'))
        #data['achievement'] = []
        user = token_to_user_course(token)


        for t in tasks:
            achievements = t.achievements.all()
            for a in achievements:
                result = engine.check_achievement(user=user, key=a.key)
                if result["new"]:
                    n = Notification (
                        name=result["name"] + " Earned",
                        description=result["description"],
                        icon=result["icon"],
                        user=user
                    )
                    n.save()

        return response
