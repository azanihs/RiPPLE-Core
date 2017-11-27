from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, CompetencyMap, QuestionScore
from questions.services import CompetencyService
from users.models import Token
from questions.models import CourseUser
from django.core.exceptions import ObjectDoesNotExist
from ripple.util import util

from django.db.models import Count
import random


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
        1: 1 if is_correct else -1,
        2: 0.25 if is_correct else -1,
        3: -0.25 if is_correct else -1,
        4: -0.75 if is_correct else -1
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

        user_competency = CompetencyService.get_user_competency_for_topics(user, topics)
        previous_score = 0
        attempt_count = 1

        if user_competency is None:
            user_competency = CompetencyService.add_competency(50, 1, user, topics)
        else:
            attempt_count = QuestionResponse.objects.filter(
                user=user, response__in=Distractor.objects.filter(question=question)).count()

            if attempt_count > 1:
                # Has attempted question before
                previous_score = QuestionScore.objects.get(
                    user=user, question=question).score

        question_score = calculate_question_score(
            attempt_count, response.response.isCorrect)

        user_competency.competency = (
            user_competency.competency * user_competency.confidence - previous_score + question_score) / (user_competency.confidence + weight)

        user_competency.confidence += weight
        user_competency.save()

        update_question_score(user, question, question_score)
        return user_competency
