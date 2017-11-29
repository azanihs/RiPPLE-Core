from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, QuestionScore
from django.db.models import Count

def get_user_competency_for_topics(user, topics):
    not_t = Topic.objects.exclude(id__in=topics)
    cu = Competency.objects.filter(user=user)
    return cu.exclude(topics__in=not_t) \
            .filter(topics__in=topics) \
            .annotate(num_topics=Count('topics')).filter(num_topics=len(topics))

def add_competency(competency, confidence, user, topics):
    c = Competency.objects.create(competency=competency, confidence=confidence, user=user)
    c.save()
    c.topics.set(topics)
    return c
