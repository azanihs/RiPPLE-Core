import random

from django.db.models import Count

import math

import numpy as np
from ripple.util import util
from users.models import CourseUser, Token
from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, QuestionScore, ReportQuestion
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
    calculate_question_score(user, answered_option.question, response)
    if answered_option.isCorrect:
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
    """ 
        calculates the questions score and updates the cached question  score. Also increments the answer count for the questions core
        Creates a QuestionScore if none exists
    """
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


def update_competency(user, question, response):
    """
        Updates the user's competency for all topic combinations in the given question
    """
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

        old_score = competency_to_score(user_competency.competency)
        new_score = old_score + (score*weight)      
        new_competency =  score_to_competency(new_score)
        user_competency.competency = new_competency
        user_competency.confidence += weight
        user_competency.save()


def get_competency_score(question, response):
    """ Calculates the competency for the exact topics"""
    topics = question.topics.all()
    user = response.user
    q_first_clean = Question.objects.annotate(num_topics=Count('topics'))
    q_second_clean = Question.objects.filter(topics__in=topics).annotate(num_topics=Count('topics'))
    question_scores = QuestionScore.objects.filter(user=user, question__in = \
            q_second_clean.filter(num_topics=len(topics),id__in=q_first_clean.filter(num_topics=len(topics)).values('id'))).order_by("-id")[:20]
    if (len(question_scores) > 0):
        past_average = 0
        for score in question_scores:
            past_average += score.score
        past_average = past_average/len(question_scores)    
    else:
        past_average = 1 
    ### When getting question wrong
    ### Easy question = less score - less weight going down
    ### Hard question = more score - more weight going down
    if response.response.isCorrect:
        difficulty = question.difficulty
    else:
        difficulty = (10 - question.difficulty)/2+5

    ### Array for dot product. Goal is to have 
    ### abs(dotProd) between 0.25 and 0.5 in 
    ### most situations
    weighted_features = [
        (difficulty/10, 0.2),
        (past_average, 0.1),
        (exp_moving_avg(0.9, question_scores), 0.3)
    ]

    feature, weight_vector = zip(*weighted_features)
    new_scores = np.dot(feature, weight_vector)

    ### Add score if correct, subtract if incorrect
    if response.response.isCorrect:
        return new_scores
    else:
        return -new_scores

def competency_to_score(competency):
    return math.log(competency/(1-competency))

#Inverse of competency_to_score
def score_to_competency(score):
    return 1 / (1 + math.exp(-score))


def exp_moving_avg(decay_factor, question_scores):
    res = 0
    counter = 0
    divisor = 0.3 *math.exp(3.64 * decay_factor)
    decay_factor = math.log(decay_factor)
    for score in question_scores:
        res += score.score*math.exp(decay_factor * counter)
        counter += 1
    return res/divisor

        

def report_question(user, request):
    request = request.get("questionReport", None)
    reason = request.get("reason", None)
    question = request.get("question", None)

    if reason is None or question is None:
        return {"error": "Please provide a reason and question ID"}

    question = Question.objects.get(pk=question)

    report = ReportQuestion(
        question=question,
        user=user,
        reason=reason
    )
    report.save()
    return {}

def get_reports(user):
    if not util.is_administrator(user):
        return {"error": "User does not have administrative permission for current context"}
    course = user.course
    reportQuestions= ReportQuestion.objects \
        .filter(author__in=CourseUser.objects.filter(course=course))
    
    return reportQuestions




