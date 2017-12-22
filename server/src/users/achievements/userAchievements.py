from django.conf import settings
from rippleAchievements.signals import achievement_unlocked
from questions.models import Question, QuestionResponse, Distractor, Competency
from rippleAchievements.models import Task
from random import randint
import sys
import abc
if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})
abstractproperty = abc.abstractproperty
abstractmethod = abc.abstractmethod

competency_threshold = settings.RUNTIME_CONFIGURATION["min_competency_value"]

################################################
# Setup reference tables linking views and tasks
################################################

class TaskReference():
    ### [viewName, viewURL, taskName]
    ref = [["add", "/questions/add", "add_question"],
        ["respond", "/questions/respond", "question_response"]
    ]

################################################
# If signal processing required
################################################

def ach_earned(sender, user, achievement, *args, **kwargs):
         #This is the signal callback at ach earned
        pass
achievement_unlocked.connect(ach_earned)


# Achievements must implement the following class
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
    def icon(self):
        pass

    @abstractproperty
    def tasks(self):
        pass

    @abstractmethod
    def evaluate(self, user, *args, **kwargs):
        pass

    def toJSON(self):
        return {"key": self.key, "name": self.name, "key": self.key, "description": self.description,
            "category": self.category, "condition": self.condition, "icon":self.icon, "bonus": self.bonus}

    def get_result(self, count, progress):
        json = self.toJSON()
        json["count"] = count
        json["progress"] = progress
        return json

class BeginnerAuthorAchievement(AbstractAchievementClass):
    name = "Beginner Question Author"
    key = "beginner_author"
    description = "Awarded for authoring 5 questions"
    category = "engagement"
    bonus = 5.0
    condition = 5
    icon = "alarm"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class IntermediateAuthorAchievement(AbstractAchievementClass):
    name = "Intermediate Question Author"
    key = "intermediate_author"
    description = "Awarded for authoring 10 questions"
    category = "engagement"
    bonus = 10.0
    condition = 10
    icon = "assessment"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class AdvancedAuthorAchievement(AbstractAchievementClass):
    name = "Advanced Question Author"
    key = "advanced_author"
    description = "Awarded for authoring 20 questions"
    category = "engagement"
    bonus = 20.0
    condition = 20
    icon = "build"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class BeginnerResponseAchievement(AbstractAchievementClass):
    name = "Beginner Response"
    key = "beginner_response"
    description = "Awarded for answering 10 questions"
    category = "engagement"
    bonus = 5.0
    condition = 10
    icon = "change_history"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).values('response').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class IntermediateResponseAchievement(AbstractAchievementClass):
    name = "Intermediate Response"
    key = "intermediate_response"
    description = "Awarded for answering 25 questions"
    category = "engagement"
    bonus = 10.0
    condition = 25
    icon = "compare_arrows"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).values('response').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class AdvancedResponseAchievement(AbstractAchievementClass):
    name = "Advanced Response"
    key = "advanced_response"
    description = "Awarded for answering 50 questions"
    category = "engagement"
    bonus = 20.0
    condition = 50
    icon = "code"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).values('response').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class BeginnerCompetencyAchievement(AbstractAchievementClass):
    name = "Beginner Competency"
    key = "beginner_competency"
    description = "Awarded for becoming competent in 1 subject"
    category = "competencies"
    bonus = 5.0
    condition = 1
    icon = "group_work"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        count = Competency.objects.filter(user=user, competency__gte=competency_threshold).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class IntermediateCompetencyAchievement(AbstractAchievementClass):
    name = "Intermediate Competency"
    key = "intermediate_competency"
    description = "Awarded for becoming competent in 3 subjects"
    category = "competencies"
    bonus = 10.0
    condition = 3
    icon = "motorcycle"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        count = Competency.objects.filter(user=user, competency__gte=competency_threshold).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class AdvancedCompetencyAchievement(AbstractAchievementClass):
    name = "Advanced Competency"
    key = "advanced_competency"
    description = "Awarded for becoming competent in 5 subjects"
    category = "competencies"
    bonus = 20.0
    condition = 5
    icon = "event_seat"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        count = Competency.objects.filter(user=user, competency__gte=competency_threshold).count()
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)


"""class BeginnerConnectionAchievement(AbstractAchievementClass):
    name = "Beginner Connection"
    key = "beginner_connect"
    description = "Awarded for making 3 connections"
    category = "connections"
    bonus = 5.0
    condition = 3
    icon = "pan_tool"
    tasks = []

    def evaluate(self, user, *args, **kwargs):
        ### Faked method
        count = user.pk/2
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class IntermediateConnectionAchievement(AbstractAchievementClass):
    name = "Intermediate Connection"
    key = "intermediate_connect"
    description = "Awarded for making 10 connections"
    category = "connections"
    bonus = 10.0
    condition = 10
    icon = "perm_identity"
    tasks = []

    def evaluate(self, user, *args, **kwargs):
        ### Faked method
        count = user.pk/2
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)

class AdvancedConnectionAchievement(AbstractAchievementClass):
    name = "Advanced Connection"
    key = "advanced_connect"
    description = "Awarded for making 20 connections"
    category = "connections"
    bonus = 20.0
    condition = 20
    icon = "record_voice_over"
    tasks = []

    def evaluate(self, user, *args, **kwargs):
        ### Faked method
        count = user.pk/2
        progress = min(100, count/float(self.condition)*100)
        return self.get_result(count, progress)
"""
