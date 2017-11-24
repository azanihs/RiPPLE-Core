from django.http import JsonResponse
from users.services.TokenService import token_valid, token_to_user_course
from django.conf import settings
from users.models import User
from rippleAchievements.models import View, Task, Achievement
from rippleAchievements.engine import engine
import json


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

class AchievementChecker(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.tasks = Task.objects.all()
        self.achievements = Achievement.objects.all()
        self.views = View.objects.all()        

    def __call__(self, request):

        ###################
        # On client request
        ###################
        token = request.META.get("HTTP_AUTHORIZATION", None)
        prefix = settings.FORCE_SCRIPT_NAME

        def pre(x):
            return request.path == (prefix + x) or request.path == (prefix + x + "/")

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
        data = json.loads(response.content.decode('utf-8'))
        data['achievement'] = None
        user = token_to_user_course(token) 
        

        for t in tasks:
            achievements = t.achievements.all() 
            data['achievement'] = []
            for a in achievements:
                data['achievement'].append(engine.check_achievement(user=user, key=a.key))


        response.content = json.dumps(data)
        return response
