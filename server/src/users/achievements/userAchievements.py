from rippleAchievements.signals import achievement_unlocked
from questions.models import Question, QuestionResponse, Distractor

def ach_earned(sender, user, achievement, *args, **kwargs):
        print(" ")
        #This is how to register a signal at ach earned!!

achievement_unlocked.connect(ach_earned)

class BeginnerAuthorAchievement(object):
    name = "Beginner Question Author"
    key = "beginnerAuthor"
    description = "Awarded for authoring 5 questions"
    bonus = 5.0
    condition = 5

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}

class IntermediateAuthorAchievement(object):
    name = "Intermediate Question Author"
    key = "intermediateAuthor"
    description = "Awarded for authoring 10 questions"
    bonus = 10.0
    condition = 10

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}

class AdvancedAuthorAchievement(object):
    name = "Advanced Question Author"
    key = "advancedAuthor"
    description = "Awarded for authoring 20 questions"
    bonus = 20.0
    condition = 20

    def evaluate(self, user, *args, **kwargs):
        count = Question.objects.filter(author=user).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}

class BeginnerResponseAchievement(object):
    name = "Beginner Response"
    key = "beginnerResponse"
    description = "Awarded for answering 10 questions"
    bonus = 5.0
    condition = 10

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}

class IntermediateResponseAchievement(object):
    name = "Intermediate Response"
    key = "intermediateResponse"
    description = "Awarded for answering 25 questions"
    bonus = 10.0
    condition = 25

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}

class AdvancedResponseAchievement(object):
    name = "Advanced Response"
    key = "advancedResponse"
    description = "Awarded for answering 50 questions"
    bonus = 20.0
    condition = 50

    def evaluate(self, user, *args, **kwargs):
        responses = QuestionResponse.objects.filter(user=user).only('id').all()
        count = Distractor.objects.filter(id__in=responses, isCorrect=True  ).count()
        progress = min(1, count/self.condition)
        return {"key":self.key, "count":count, "progress":progress}
