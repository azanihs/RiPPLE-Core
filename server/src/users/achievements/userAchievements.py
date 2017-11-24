from rippleAchievements.signals import achievement_unlocked
from questions.models import Question, QuestionResponse, Distractor
from rippleAchievements.models import Task
import sys
if sys.version_info[0] < 3:
    from abc import ABCMeta, abstractmethod
else:
    from abc import ABC, abstractmethod, abstractproperty

################################################
# Setup reference tables linking views and tasks
################################################

class TaskReference():
    ### [viewName, viewURL, taskName]
    ref = [["add", "/questions/add", "addQuestion"],
        ["respond", "/questions/respond", "questionResponse"]
    ]

################################################
# If signal processing required
################################################

def ach_earned(sender, user, achievement, *args, **kwargs):
         #This is the signal callback at ach earned
        pass
achievement_unlocked.connect(ach_earned)


# Achievements must implement the following class
# Python 2.7 implementation is at the bottom of the file
if (sys.version_info[0] > 3):
    class AbstractAchievementClass(ABC):
        @abstractproperty
        def name(self):
            pass
        
        @abstractproperty
        def key(self):
            pass

        @abstractproperty
        def description(self):
            pass

        @abstractproperty
        def category(self):
            pass

        @abstractproperty
        def bonus(self):
            pass

        @abstractproperty
        def condition(self):
            pass
            
        @abstractproperty
        def tasks(self):
            pass

        @abstractmethod
        def evaluate(self, user, *args, **kwargs):
            pass

        def toJSON(self):
            return {"name": self.name, "key": self.key, "description": self.description, 
                "category": self.category, "bonus": self.bonus}

        def getResult(self, count, progress):
            json = self.toJSON()
            json["count"] = count
            json["progress"] = progress
            return json

class BeginnerAuthorAchievement(AbstractAchievementClass):
    name = "Beginner Question Author"
    key = "beginnerAuthor"
    description = "Awarded for authoring 5 questions"
    category = "Engagement"
    bonus = 5.0
    condition = 5
    tasks = ["addQuestion"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)

class IntermediateAuthorAchievement(AbstractAchievementClass):
    name = "Intermediate Question Author"
    key = "intermediateAuthor"
    description = "Awarded for authoring 10 questions"
    category = "Engagement"
    bonus = 10.0
    condition = 10
    tasks = ["addQuestion"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)

class AdvancedAuthorAchievement(AbstractAchievementClass):
    name = "Advanced Question Author"
    key = "advancedAuthor"
    description = "Awarded for authoring 20 questions"
    category = "Engagement"
    bonus = 20.0
    condition = 20
    tasks = ["addQuestion"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)

class BeginnerResponseAchievement(AbstractAchievementClass):
    name = "Beginner Response"
    key = "beginnerResponse"
    description = "Awarded for answering 10 questions"
    category = "Engagement"
    bonus = 5.0
    condition = 10
    tasks = ["questionResponse"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)

class IntermediateResponseAchievement(AbstractAchievementClass):
    name = "Intermediate Response"
    key = "intermediateResponse"
    description = "Awarded for answering 25 questions"
    category = "Engagement"
    bonus = 10.0
    condition = 25
    tasks = ["questionResponse"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)

class AdvancedResponseAchievement(AbstractAchievementClass):
    name = "Advanced Response"
    key = "advancedResponse"
    description = "Awarded for answering 50 questions"
    category = "Engagement"
    bonus = 20.0
    condition = 50
    tasks = ["questionResponse"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True  ).count()
        progress = min(1, count/self.condition)
        return self.getResult(count, progress)



if sys.version_info[0] < 3:
    class AbstractAchievementClass(object):
        __metaclass__ = ABCMeta
        @abstractproperty
        def name(self):
            pass
        
        @abstractproperty
        def key(self):
            pass

        @abstractproperty
        def description(self):
            pass

        @abstractproperty
        def category(self):
            pass

        @abstractproperty
        def bonus(self):
            pass

        @abstractproperty
        def condition(self):
            pass
            
        @abstractproperty
        def tasks(self):
            pass

        @abstractmethod
        def evaluate(self, user, *args, **kwargs):
            pass

        def toJSON(self):
            return {"name": self.name, "key": self.key, "description": self.description, 
                "category": self.category, "bonus": self.bonus}

        def getResult(self, count, progress):
            json = self.toJSON()
            json["count"] = count
            json["progress"] = progress
            return json