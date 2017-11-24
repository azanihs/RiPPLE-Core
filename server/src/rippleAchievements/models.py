import importlib
import types
import inspect
import logging

from django.core.exceptions import ImproperlyConfigured
from users.models import CourseUser
from django.conf import settings
from django.db import models



from appconf import AppConf

logger = logging.getLogger(__name__)


def check_achievement_class(cls):
    return [attribute for attribute in ['name', 'key', 'description', 'category', 'bonus', 'condition', 'tasks', 'evaluate'] if not hasattr(cls, attribute)]


def load_classes(classes=settings.ACHIEVEMENT_CLASSES, *args, **kwargs):
    # if we're called during south migration ignore every app
    # until we get notified that the achievements app
    # was properly loaded
    current_app = kwargs.get('app', None)
    # this case is when we're using south migrations
    if type(current_app) is str and current_app != 'achievements':
        return
    # otherwise when we use plain syncdb :
    if type(current_app) is types.ModuleType and current_app.__name__ != 'achievements.models':
        return
    # Setup tasks
    setupTasks(classes)
    from rippleAchievements.engine import engine
    for achievement_module in classes:
        try:
            module = importlib.import_module(achievement_module)
            clses = [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and name.endswith('Achievement')]
            for cl in clses:
                errors = check_achievement_class(cl)
                if errors:
                    message = "Achievement class '%s' in '%s' has missing attributes : %s" % (cl.__name__, module.__name__, ",".join(errors))
                    logger.error(message)
                    raise ImproperlyConfigured(message)
                else:
                    logger.info("Registering achievement class %s..." % (cl))
                    engine.register_achievement(cl)
        except ImproperlyConfigured:
            raise
        except Exception as exc:
            logger.error("Exception caught while trying to register achievements class %s " % exc)
            raise ImproperlyConfigured("ACHIEVEMENT_CLASSES attribute must be set properly for them to be loaded into the engine : %s" % exc)

def setupTasks(classes):
    Task.objects.all().delete()
    View.objects.all().delete()
    module = importlib.import_module(classes[0])
    clses = [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and name == 'TaskReference']
    for cl in clses:
        ref = cl.ref
        for i in ref:
            addView(i[0], i[1], i[2])

def addView(view, url, task):
    (v, created) = View.objects.get_or_create(
        view=view,
        defaults={"url":url}
    )
    if not created:
        v.url = url
    v.save()
    t = Task.objects.get_or_create(
        task=task
    )[0]
    t.save()
    t.views.add(v)


class Achievement(models.Model):
    """ These objects are what people are earning when contributing """
    name = models.CharField(max_length=75)
    key = models.CharField(max_length=75, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(default="", max_length=75)
    bonus = models.IntegerField(default=0)
    condition = models.IntegerField(default=1)
    callback = models.TextField()

    def __unicode__(self):
        return "Achievement(%s, %s)" % (self.name, self.bonus)


class UserAchievement(models.Model):
    user = models.ForeignKey(CourseUser)
    achievement = models.ForeignKey(Achievement, related_name="userachievements")
    registered_at = models.DateTimeField(auto_now_add=True)


class AchievementEngineConf(AppConf):
    """ Configuration class used by Django AppConf to ease the setup"""
    USE_CELERY = False
    CLASSES = []

    class Meta:
        prefix = 'achievement'

    def configure_classes(self, value):
        pass

class View(models.Model):
    view = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=30, unique=True, default="/"+str(view))

class Task(models.Model):
    task = models.CharField(max_length=30, unique=True)
    views = models.ManyToManyField(View)
    achievements = models.ManyToManyField(Achievement)

# connect to the end of the syncdb command signal to reload achievements at that time.
if 'south' in settings.INSTALLED_APPS:
    from south.signals import post_migrate
    post_migrate.connect(load_classes)
else:
    from django.db.models.signals import post_migrate
    post_migrate.connect(load_classes)
