from django.conf import settings
from django.db import IntegrityError, transaction
from django.core.exceptions import ImproperlyConfigured
from rippleAchievements.models import Achievement, Task
from rippleAchievements.utils import construct_callback, check_achievement_plain
from rippleAchievements.signals import achievement_registered
import logging

logger = logging.getLogger(__name__)

class AchievementEngine(object):
    def register_achievement(self, cls):
        try:
            with transaction.atomic():
                """ Register a new achievement into the engine and database"""
                (obj, created) = Achievement.objects.get_or_create(key=cls.key,  defaults={
                    'name': cls.name,
                    'description': cls.description,
                    'category': cls.category,
                    'bonus': cls.bonus,
                    'condition': cls.condition,
                    'icon': cls.icon,
                    'callback': construct_callback(cls)})
                
                if not created:
                    # update the object if key didn't change :
                    obj.name = cls.name
                    obj.description = cls.description
                    obj.category = cls.category
                    obj.bonus = cls.bonus
                    obj.condition = cls.condition
                    obj.icon = cls.icon
                    obj.callback = construct_callback(cls)
                    obj.save()
                for t in cls.tasks:
                    tObj = Task.objects.get(task=t)
                    tObj.achievements.add(obj)
                    tObj.save()
                achievement_registered.send(sender=self, achievement_class=cls)
        except IntegrityError as e:
            raise IntegrityError(str(e))
        except Exception as e:
            raise Exception(str(e))

    def check_achievement(self, user, key, *args, **kwargs):
        """
        Check synchronously or asynchronously if according to a specific context
        an achievement has been unlocked
        """
        if user:
            if settings.ACHIEVEMENT_USE_CELERY:
                # do not try to import if celery is not defined
                from rippleAchievements.tasks import check_achievement_task
                return check_achievement_task.delay(self, user, key, *args, **kwargs)
            else:
                return check_achievement_plain(self, user, key, *args, **kwargs)
        else:
            logger.info("trying to check an achievement for an un-logged user")


# create the engine
engine = AchievementEngine()

