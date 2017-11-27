from rippleAchievements.signals import achievement_unlocked
from questions.models import Question, QuestionResponse, Distractor
from rippleAchievements.models import Task
import sys
import abc
if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})
abstractproperty = abc.abstractproperty
abstractmethod = abc.abstractmethod

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
            "category": self.category, "icon":self.icon, "bonus": self.bonus}

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
    icon = "Bronze"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)

class IntermediateAuthorAchievement(AbstractAchievementClass):
    name = "Intermediate Question Author"
    key = "intermediate_author"
    description = "Awarded for authoring 10 questions"
    category = "engagement"
    bonus = 10.0
    condition = 10
    icon = "Silver"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)

class AdvancedAuthorAchievement(AbstractAchievementClass):
    name = "Advanced Question Author"
    key = "advanced_author"
    description = "Awarded for authoring 20 questions"
    category = "engagement"
    bonus = 20.0
    condition = 20
    icon = "Gold"
    tasks = ["add_question"]

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)

class BeginnerResponseAchievement(AbstractAchievementClass):
    name = "Beginner Response"
    key = "beginner_response"
    description = "Awarded for answering 10 questions"
    category = "engagement"
    bonus = 5.0
    condition = 10
    icon = "Monkey"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)

class IntermediateResponseAchievement(AbstractAchievementClass):
    name = "Intermediate Response"
    key = "intermediate_response"
    description = "Awarded for answering 25 questions"
    category = "engagement"
    bonus = 10.0
    condition = 25
    icon = "Spider"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)

class AdvancedResponseAchievement(AbstractAchievementClass):
    name = "Advanced Response"
    key = "advanced_response"
    description = "Awarded for answering 50 questions"
    category = "engagement"
    bonus = 20.0
    condition = 50
    icon = "Web"
    tasks = ["question_response"]

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True  ).count()
        progress = min(100, count/self.condition*100)
        return self.get_result(count, progress)