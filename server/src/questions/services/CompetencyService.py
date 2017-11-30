from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, QuestionScore
from django.db.models import Count

def get_user_competency_for_topics(user, topics):
    t_count_1 = Competency.objects.annotate(num_topics=Count('topics'))
    t_count_2 = Competency.objects.filter(topics__in=topics).annotate(num_topics=Count('topics'))
    t_comp = t_count_2.filter(num_topics=len(topics), id__in=t_count_1.filter(num_topics=len(topics)).values('id'))
    cu = Competency.objects.filter(user=user)
    return cu.filter(id__in=t_comp)


def add_competency(competency, confidence, user, topics):
    c = Competency.objects.create(competency=competency, confidence=confidence, user=user)
    c.save()
    c.topics.set(topics)
    return c
