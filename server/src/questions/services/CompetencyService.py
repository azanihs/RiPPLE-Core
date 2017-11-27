from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, CompetencyMap, QuestionScore

def get_topics_id(topics):
    competency_representation = CompetencyMap.objects.filter(topic__in=topics)

    if len(competency_representation) != len(topics):
        auto_id = None
        for i in topics:
            comp_map = CompetencyMap.objects.create(topic=i, aggregate_id=auto_id)
            if auto_id is None:
                auto_id = comp_map.id
                comp_map.aggregate_id = auto_id
                comp_map.save()

        return comp_map.aggregate_id
    else:
        return competency_representation.first().aggregate_id


def get_user_competency_for_topics(user, topics):
    topics_id = get_topics_id(topics)
    try:
        competency = Competency.objects.get(user=user, topics=topics_id)
    except Competency.DoesNotExist:
        return None

    return competency

def add_competency(competency, confidence, user, topics):
    comp_map_id = get_topics_id(topics)
    return Competency.objects.create(competency=competency, confidence=confidence, user=user, topics=comp_map_id)
