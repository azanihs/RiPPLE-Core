from ..models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, CompetencyMap, QuestionScore
from users.models import Token
from questions.models import CourseUser
from django.core.exceptions import ObjectDoesNotExist
from ripple.util import util

from django.db.models import Count
import random

import math

import numpy as np

def leaderboard_sort(class_instance, user_column):
    query = class_instance.objects.values(
        user_column).annotate(total=Count(user_column))
    return [x for x in query]


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


def all_questions():
    return Question.objects.all()


def get_course_topics(course):
    return Topic.objects.filter(course=course).distinct()


def get_questions(id):
    try:
        return Question.objects.get(pk=id)
    except ObjectDoesNotExist:
        return None


def respond_to_question(distractor_id, user):
    try:
        answered_option = Distractor.objects.get(pk=distractor_id)
    except Distractor.DoesNotExist:
        return None

    response = QuestionResponse(
        user=user,
        response=answered_option
    )
    response.save()

    update_competency(user, answered_option.question, response)
    return True


def rate_question(distractor_id, response, user):
    difficulty = response.get("difficulty", None)
    quality = response.get("quality", None)
    try:
        answered_option = Distractor.objects.get(pk=distractor_id)
        found = QuestionRating.objects.filter(
            user_id=user.id, response_id=distractor_id
        ).first()

        if found is None:
            QuestionRating(
                quality=quality,
                difficulty=difficulty,
                response=answered_option,
                user=user
            ).save()
            return True
        else:
            # Update existing response
            found.quality = quality
            found.difficulty = difficulty
            found.save()
            return True
    except ObjectDoesNotExist:
        return None


def calculate_question_score(attempts, is_correct):

    score_map = {
        1: 1 if is_correct else 0,
        2: 0.75 if is_correct else 0,
        3: 0.5 if is_correct else 0,
        4: 0.25 if is_correct else 0
    }
    return score_map[min(4, attempts)]


def update_question_score(user, question, new_score):
    """
        Helper method to update the cached QuestionScore for a users question to new_score. Also increments the answer count for the question score
        Creates a QuestionScore is none exists
    """
    try:
        cached_question_score = QuestionScore.objects.get(
            user=user, question=question)
        cached_question_score.score = new_score
        cached_question_score.number_answers += 1
        cached_question_score.save()
    except QuestionScore.DoesNotExist:
        QuestionScore(user=user, question=question, number_answers=1,
                      score=new_score).save()


def update_competency(user, question, response):
    """
        Updates the users competency for all topic combinations in the given question
    """
    # Weigh each topic
    weights = util.topic_weights(question.topics.all())
    for i in weights:
        topics = i["topics"]
        weight = i["weight"]

        mapped_competencies = CompetencyMap.objects.filter(
            user=user, topic__in=topics)

        previous_score = 0
        attempt_count = 1
        if len(topics) == mapped_competencies.count():
            attempt_count = QuestionResponse.objects.filter(
                user=user, response__in=Distractor.objects.filter(question=question)).count()

            user_competency = Competency.objects.get(
                pk=mapped_competencies.first().for_competency_id)

            if attempt_count > 1:
                # Has not attempted question before
                previous_score = QuestionScore.objects.get(
                    user=user, question=question).score
        else:
            user_competency = Competency.objects.create(
                competency=0.5, confidence=1)

            for topic in topics:
                CompetencyMap(
                    user=user,
                    topic=topic,
                    for_competency=user_competency
                ).save()

        question_score = calculate_question_score(
            attempt_count, response.response.isCorrect)

        total_correct = 1
        total_incorrect = 1
        
        question_count = QuestionResponse.objects.count()
        for response in QuestionResponse.objects.all():
            if response.response.isCorrect:
                total_correct += 1
            else:
                total_incorrect += 1

        if response.response.isCorrect == False:
            difficulty = 10 - response.response.question.difficulty
        else:
            difficulty = response.response.question.difficulty

        weighted_features = [
            (difficulty/10, 0.25),
            (previous_score, 0.3),
            (math.log(total_incorrect), 0.35),
            (math.log(total_correct), 0.35),
            (exp_moving_avg(0.33), 0.35),
            (exp_moving_avg(0.1), 0.25),
            (float(total_correct / question_count), 0.30),
            (user_competency.competency, 0.30)
        ]

        feature, weight_vector = zip(*weighted_features)

        scores = np.dot(feature, weight_vector)

        new_competency = 1 / (1 + math.exp(-scores))

        if response.response.isCorrect == False:
            user_competency.competency = (user_competency.competency + (1 - new_competency))/2
            if user_competency.competency < 0.1:
                user_competency.competency = 0.1
        else:
            user_competency.competency = (user_competency.competency + new_competency)/2

        user_competency.save()

        update_question_score(user, question, question_score)
        return user_competency

def exp_moving_avg(weight):
    ewma = 0.5
    for response in QuestionResponse.objects.all():
        correct = 0
        if response.response.isCorrect:
            correct += 1
        ewma = weight * correct + (1 - weight) * ewma
 
    return ewma

"""Current implementation of the khan academy normalization equation """
""" refer to http://david-hu.com/2011/11/02/how-khan-academy-is-using-machine-learning-to-assess-student-mastery.html? """
# count = 10

        # X = np.zeros(10)
        # Y = np.zeros(10)

        # for i in range(0,10):
        #     QuestionService.respond_to_question(2, author)
        #     X[i] = Competency.objects.all().first().competency
        #     Y[i] = i+1
        
        # A, B = np.polyfit(X, np.log(Y),1)

        # A /= (A * np.exp(B * 0.90))

        # print(A)
        # print(B)
        # print(sorted((A * np.exp(B * 0.90), 0.0, 1.0))[1])
        