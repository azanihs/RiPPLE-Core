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
        Updates the user's competency for all topic combinations in the given question
    """
    # Weigh each topic
    
    question_score = calculate_question_score(
            attempt_count, response.response.isCorrect)

    total_correct = 1
    total_incorrect = 1

    q_first_clean = Question.objects.annotate(num_topics=Count('topics'))
    q_second_clean = Question.objects.filter(topics__in=topics).annotate(num_topics=Count('topics'))
    question_responses = QuestionResponse.objects.filter(user=user, response__in=Distractor.objects.filter(question__in = \
                    q_second_clean.filter(num_topics=len(topics),id__in=q_first_clean.filter(num_topics=len(topics)).values('id'))))


    if len(question_responses) > 0:

            for response in question_responses:
                if response.response.isCorrect:
                    total_correct += 1
                else:
                    total_incorrect += 1

            if response.response.isCorrect == False:
                difficulty = 10 - response.response.question.difficulty
            else:
                difficulty = response.response.question.difficulty

            print("WEIGHT:" + str(weight))
            print(topics)

            weighted_features = [
                (difficulty/10, 0.25),
                (previous_score, 0.3),
                (math.log(user_competency.confidence), 0.25),
                (math.log(total_incorrect), 0.35),
                (math.log(total_correct), 0.35),
                (exp_moving_avg(0.33), 0.35),
                (exp_moving_avg(0.1), 0.25),
                (float(total_correct / len(question_responses)), 0.30),
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

        user_competency.confidence += weight

        user_competency.save()

        update_question_score(user, question, question_score)
    
    
    weights = util.topic_weights(question.topics.all())


    queryset_topics = question.topics.all()
    weights = util.topic_weights(queryset_topics)

    for i in weights:
        topics = queryset_topics.filter(id__in=[x.id for x in i["topics"]])
        weight = i["weight"]

        user_competency = CompetencyService.get_user_competency_for_topics(user, topics)
        previous_score = 0
        attempt_count = 1

        if user_competency is None or len(user_competency) == 0:
            user_competency = CompetencyService.add_competency(50, 1, user, topics)
        else:
            user_competency = user_competency[0]
            attempt_count = QuestionResponse.objects.filter(
                user=user, response__in=Distractor.objects.filter(question=question)).count()

            if attempt_count > 1:
                # Has attempted question before
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

        # question_responses = QuestionResponse.objects.filter(user=user, response__in=Distractor.objects.filter(question__in = \
        #                 Question.objects.filter(topics__in = topics)))
        
        print(question_responses)

        


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
        
        update_question_score(user, question, question_score)
