import random

from django.db.models import Count

import math

import numpy as np
from ripple.util import util
from users.models import CourseUser, Token
from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, QuestionScore
from questions.services import CompetencyService

def leaderboard_sort(class_instance, user_column):
    query = class_instance.objects.values(
        user_column).annotate(total=Count(user_column))
    return [x for x in query]

def question_response_distribution(question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return {"error": "Question ID " + str(question_id) + " does not exist"}

    question_distractors = Distractor.objects.filter(question=question)
    question_responses = QuestionResponse.objects.filter(response__in=question_distractors)
    total_responses = question_responses.count()
    response_distribution = {}

    for i in question_distractors:
        distractor_response_count = question_responses.filter(response=i).count()
        if total_responses is 0:
            response_distribution[i.id] = 0
        else:
            response_distribution[i.id] = (distractor_response_count / total_responses) * 100

    return response_distribution

def get_course_leaders(course, sort_field, sort_order, limit=25):
    def lookup_total(fieldName, user_id, data):
        for dict_item in data:
            entry = dict_item.get(fieldName, None)
            if entry == user_id:
                return dict_item.get("total", 0)
        return 0

    course_users = CourseUser.objects.filter(course=course)
    # Cache database calls
    question_counts = leaderboard_sort(Question, "author_id")
    response_counts = leaderboard_sort(QuestionResponse, "user_id")
    rating_counts = leaderboard_sort(QuestionRating, "user_id")
    login_counts = leaderboard_sort(Token, "user_id")

    leaderboard_users = [{
        "name": u.user.first_name,
        "image": u.user.image,
        "reputation": random.randint(0, 100),
        "questionsAuthored": lookup_total("author_id", u.id, question_counts),
        "questionsAnswered": lookup_total("user_id", u.id, response_counts),
        "questionsCommented": random.randint(0, 100),
        "questionsViewed": random.randint(0, 100),
        "questionsRated": lookup_total("user_id", u.id, rating_counts),

        "connectionsMade": random.randint(0, 100),
        "logins": lookup_total("user_id", u.id, login_counts)
    } for u in course_users]

    if len(leaderboard_users) > 0 and sort_field in leaderboard_users[0]:
        should_reverse = sort_order == "DESC"
        leaderboard_users = sorted(
            leaderboard_users, key=lambda k: k[sort_field], reverse=should_reverse)

    if limit == -1:
        return leaderboard_users
    return leaderboard_users[0:limit]


def get_course_topics(course):
    return Topic.objects.filter(course=course).distinct()


def get_question(id):
    try:
        return Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return None


def respond_to_question(distractor_id, user):
    try:
        answered_option = Distractor.objects.get(pk=distractor_id)
    except Distractor.DoesNotExist:
        return False

    if answered_option.question.author.course != user.course:
        raise ValueError("Question course and user course do not match")

    response = QuestionResponse(
        user=user,
        response=answered_option
    )
    response.save()

    update_competency(user, answered_option.question, response)
    return True

def update_running_mean(value, count, new_weight):
    return (value * count + new_weight) / (count + 1)

def update_mean(value, previous, count, new_weight):
    return value + ((new_weight - previous) / count)

def rate_question(distractor_id, user_ratings, user):
    difficulty = user_ratings.get("difficulty", None)
    quality = user_ratings.get("quality", None)
    try:
        answered_option = Distractor.objects.get(pk=distractor_id)
        found = QuestionRating.objects.filter(
            user_id=user.id, response_id=distractor_id
        ).first()
        question = answered_option.question

        if found is None:
            question_rating = QuestionRating(response=answered_option, user=user)
        else:
            question_rating = found

        if quality is not None:
            if found is None or (found is not None and found.quality is None):
                question.quality = update_running_mean(question.quality, question.qualityCount, quality)
                question.qualityCount += 1
            elif found is not None and found.quality is not None:
                question.quality = update_mean(question.quality, found.quality, question.qualityCount, quality)
            question_rating.quality = quality

        if difficulty is not None:
            if found is None or (found is not None and found.difficulty is None):
                question.difficulty = update_running_mean(question.difficulty, question.difficultyCount, difficulty)
                question.difficultyCount += 1
            elif found is not None and found.difficulty is not None:
                question.difficulty = update_mean(question.difficulty, found.difficulty, question.difficultyCount, difficulty)
            question_rating.difficulty = difficulty

        question_rating.save()
        question.save()
        return True
    except Distractor.DoesNotExist:
        return False


def calculate_question_score(user, question, response):
    try:
        question_score = QuestionScore.objects.get(
            user=user, question=question)
    except QuestionScore.DoesNotExist:
        question_score = QuestionScore(user=user, question=question, 
                number_answers=0, score=0)
        question_score.save()

    is_correct = response.response.isCorrect
    if not is_correct:
        question_score.number_answers += 1
        question_score.score = 0
        question_score.save()
        return

    score_map = {
        1: 1 if is_correct else 0,
        2: 0.75 if is_correct else 0,
        3: 0.5 if is_correct else 0,
        4: 0.25 if is_correct else 0
    }

    question_score.score = score_map[min(4,question_score.number_answers+1)]
    question_score.number_answers = 0
    question_score.save()

def update_question_score(user, question, new_score):
    """
        Helper method to update the cached QuestionScore for a users question to new_score. Also increments the answer count for the question score
        Creates a QuestionScore is none exists
    """
    try:
        cached_question_score = QuestionScore.objects.get(
            user=user, question=question)
        cached_question_score.score = new_score
        if new_score > 0:
            cached_question_score.number_answers = 0
        else:
            cached_question_score.number_answers += 1      
        cached_question_score.save()
    except QuestionScore.DoesNotExist:
        QuestionScore(user=user, question=question, number_answers=1,
                      score=new_score).save()


def update_competency(user, question, response):
    """
        Updates the user's competency for all topic combinations in the given question
    """
    calculate_question_score(user, question, response)

    queryset_topics = question.topics.all()

    score = get_competency_score(question, response)
    calculate_children_competency(user, queryset_topics, score)
    
        

def calculate_children_competency(user, queryset_topics, score):
    """ Updates children competencies"""
    # Weigh each topic
    weights = util.topic_weights(queryset_topics)
    for i in weights:
        topics = queryset_topics.filter(id__in=[x.id for x in i["topics"]])
        weight = i["weight"]

        user_competency = CompetencyService.get_user_competency_for_topics(user, topics)

        if user_competency is None or len(user_competency) == 0:
            user_competency = CompetencyService.add_competency(0.5, 0, user, topics)
        else:
            user_competency = user_competency[0]

        old_score = math.log(user_competency.competency/(1-user_competency.competency))
        new_score = old_score + (score*weight)      
        new_competency =  1 / (1 + math.exp(-new_score))
        user_competency.competency = new_competency
        user_competency.confidence += weight
        user_competency.save()


def get_competency_score(question, response):
    """ Calculates the competency for the exact topics"""
    topics = question.topics.all()
    user = response.user
    #### Update to get question scores, not responses.
    q_first_clean = Question.objects.annotate(num_topics=Count('topics'))
    q_second_clean = Question.objects.filter(topics__in=topics).annotate(num_topics=Count('topics'))
    question_responses = QuestionResponse.objects.filter(user=user, response__in=Distractor.objects.filter(question__in = \
            q_second_clean.filter(num_topics=len(topics),id__in=q_first_clean.filter(num_topics=len(topics)).values('id'))))
    
    ### This will be averaging question scores
    if (len(question_responses) > 0):
        correct = 0
        for resp in question_responses: 
            if resp.response.isCorrect:
                correct += 1
        correct = correct/len(question_responses)
    else:
        correct = 0.5
    #############################################

    ### Easy question = less score
    ### Hard question = more score
    if response.response.isCorrect:
        difficulty = question.difficulty
    else:
        difficulty = 10 - question.difficulty

    print(difficulty)
    ### Array for dot product. Goal is to have 
    ### abs(dotProd) between 0.25 and 0.5 in 
    ### most situations

    ### Important tests: 
    # How many correct to high
    # How many incorrect to low
    # How many to recover from low to high, and reverse 
    # How does alternating questions work
    # Questions of varying difficutly
    ### 
    weighted_features = [
        (difficulty/10, 0.30),
        (correct, 0.10),
        (exp_moving_avg(0.33, question_responses), 0.20),
        (exp_moving_avg(0.1, question_responses), 0.15)
    ]

    feature, weight_vector = zip(*weighted_features)
    new_scores = np.dot(feature, weight_vector)

    ### Add score if correct, subtract if incorrect
    if response.response.isCorrect:
        return new_scores
    else:
        return -new_scores
  

def exp_moving_avg(weight, questions):
    ewma = 0.3
    for response in questions:
        correct = 0
        if response.response.isCorrect:
            correct += 1
        ewma = weight * correct + (1 - weight) * ewma
    return ewma

        