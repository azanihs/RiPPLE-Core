import random
import math
import numpy as np
import pytz as timezone
from datetime import datetime

from django.db.models import Count, Min, Max
from django.db import IntegrityError, transaction

from ripple.util import util
from users.models import CourseUser, Token, User
from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse,\
    Competency, QuestionScore, ReportQuestion, ReportReason, ReportQuestionList, DeletedQuestion
from rippleAchievements.models import UserAchievement
from questions.services import CompetencyService, AuthorService

_epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

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
    total_responses = question_responses.values('user_id').distinct().count()
    response_distribution = {}

    for i in question_distractors:
        first_response = question_responses.values('user_id').annotate(first=Min('id')).values_list('first', flat=True)
        distractor_response_count = question_responses.filter(id__in=first_response,  response=i).count()
        if total_responses is 0:
            response_distribution[i.id] = 0
        else:
            response_distribution[i.id] = (distractor_response_count / total_responses) * 100
    return response_distribution

def get_course_leaders(course, sort_field, sort_order, user, limit=25):
    def lookup_total(fieldName, user_id, data):
        for dict_item in data:
            entry = dict_item.get(fieldName, None)
            if entry == user_id:
                return dict_item.get("total", 0)
        return 0

    course_users = CourseUser.objects.filter(course=course)

    question_counts = leaderboard_sort(Question, "author_id")

    response_SQL = "SELECT 1 as id, qr.user_id, COUNT(DISTINCT d.question_id) as 'total' FROM "+\
    "questions_questionresponse qr, questions_distractor d WHERE qr.response_id = d.id GROUP BY qr.user_id"
    response_qry = QuestionResponse.objects.raw(response_SQL)
    response_counts = []
    for r in response_qry:
        response_counts.append({
            "user_id": r.user_id,
            "total": r.total
        })

    first_response_SQL = "SELECT 1 as id, qr.user_id, COUNT(*) as 'total' FROM questions_questionresponse qr, "+\
        "questions_question q, questions_distractor d WHERE d.question_id = q.id AND qr.response_id=d.id AND "+\
        "d.isCorrect=1 AND qr.id IN (SELECT MIN(qr.ID) FROM questions_questionresponse qr, questions_question q, "+\
        "questions_distractor d where d.question_id = q.id AND qr.response_id=d.id GROUP BY qr.user_id, "+\
        "q.id) GROUP BY qr.user_id"
    first_response_qry = QuestionResponse.objects.raw(first_response_SQL)
    first_response_counts=[]
    for r in first_response_qry:
        first_response_counts.append({
            "user_id": r.user_id,
            "total": r.total
        })

    rating_counts = leaderboard_sort(QuestionRating, "user_id")

    achievement_counts = leaderboard_sort(UserAchievement, "user_id")

    leaderboard_users = [{
        "rank": u.id,
        "name": u.user.first_name,
        "image": u.user.image,
        "questionsAuthored": lookup_total("author_id", u.id, question_counts),
        "questionsAnswered": lookup_total("user_id", u.id, response_counts),
        "questionsAnsweredCorrectly": lookup_total("user_id", u.id, first_response_counts),
        "questionsRated": lookup_total("user_id", u.id, rating_counts),
        "achievementsEarned": lookup_total("user_id", u.id, achievement_counts)
    } for u in course_users]

    if len(leaderboard_users) > 0 and sort_field in leaderboard_users[0]:
        should_reverse = sort_order == "DESC"
        leaderboard_users = sorted(
            leaderboard_users, key=lambda k: k[sort_field], reverse=should_reverse)

    found = 0
    for i in leaderboard_users:
    if not util.is_administrator(user):
        for i in range(0,len(leaderboard_users)):
            if leaderboard_users[i]["rank"] == user.id:
                found = i
                leaderboard_users[i]["id"] = user.id
            leaderboard_users[i]["rank"] = i+1

    if limit == -1:
        return leaderboard_users

    leaderboard = leaderboard_users[0:limit]
    if found >= limit:
        leaderboard.append(leaderboard_users[found])
    return leaderboard


def get_course_topics(course):
    return Topic.objects.filter(course=course).distinct()


def get_random_question(user):
    course = user.course
    course_questions = Question.objects.filter(author__in=CourseUser.objects.filter(course=course))

    count = course_questions.aggregate(count=Count('id'))['count']
    random_index = random.randint(0, count - 1)
    return course_questions.all()[random_index]

def get_question_by_id(user, id):
    try:
        question = Question.objects.get(pk=id)
        if question.author.course != user.course:
            return None
        q_JSON =  question.toJSON()
        if util.is_administrator(user) or question.author == user:
            q_JSON["canEdit"] = True
        else:
            q_JSON["canEdit"] = False
        return q_JSON
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
            user_competency = CompetencyService.add_competency(0.1, 0, user, topics)
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

    if reason is None or len(reason) == 0 or question is None:
        return {"error": "Please provide a reason and question ID"}

    question = Question.objects.get(pk=question)

    report = ReportQuestion(
        question=question,
        user=user
    )
    report.save()

    for r in reason:
        try:
            report_reason = ReportReason.objects.get(course=user.course, reason=r)
        except ReportReason.DoesNotExist:
            report_reason = ReportReason.objects.get(course=user.course, reason="custom")
        report_reason = ReportQuestionList (
            report_question = report,
            report_reason = report_reason,
            reason_text = r
        )
        report_reason.save()
    return {}

def get_reason_list(user):
    course = user.course
    reasons = ReportReason.objects.filter(course=course)
    r_list = [r.reason for r in reasons if r.reason != "custom"]
    return {"reasonList": r_list}

def report_aggregate(user):
    #if not util.is_administrator(user):
    #    return {"error": "User does not have administrative permission for current context"}
    course = user.course
    report_questions = ReportQuestion.objects \
        .filter(user__in=CourseUser.objects.filter(course=course))

    report_aggregates = report_questions.values("question")\
            .annotate(total=Count("question")).annotate(last_report=Max("created_at")).order_by("-total")
    reports = []
    for q in report_aggregates:
        reports.append({
            "questionID": q["question"],
            "totalReports": q["total"],
            "lastReport": (q["last_report"].replace(tzinfo=timezone.utc) - _epoch).total_seconds()
        })
    return reports

def all_reports(user):
    reports = []
    aggregates = report_aggregate(user)
    reports.append(aggregates)
    for rep in aggregates:
        qid = rep["questionID"]
        q_reports = ReportQuestion.objects.filter(question=qid).order_by("-id")
        report_list = []
        for r in q_reports:
            report_list.append(r.toJSON_summary())
        reports.append(report_list)
    reports = {"reports": reports}
    return reports

def delete_question(user, qid):
    try:
        question = Question.objects.get(id=qid)
        if (util.is_administrator(user) or user == question.author):
            with transaction.atomic():
                deleted = make_deleted_question(question)
                deleted.topics.set(question.topics.all())
                question.delete()
            return {"data": {}}
        else:
            return {"error": "Permission Denied"}
    except Question.DoesNotExist:
        return {"error": "Question does not exist"}
    except IntegrityError as e:
        return {"error": str(e)}


def update_question(post_request, root_path, user, qid):
    try:
        question = Question.objects.get(id=qid)
        if (util.is_administrator(user) or user == question.author):
            with transaction.atomic():
                deleted = make_deleted_question(question)
                deleted.topics.set(question.topics.all())
                return AuthorService.add_question(post_request, root_path, user, question)
        else:
            return {"state": "Error", "error": "Permission Denied"}
    except Question.DoesNotExist:
        return {"state": "Error", "error": "Question does not exist"}
    except IntegrityError as e:
        return {"state": "Error", "error": str(e)}

def make_deleted_question(question):
    d_question = DeletedQuestion(
        content = question.content,
        explanation = question.explanation,
        difficulty = question.difficulty,
        quality = question.quality,
        difficultyCount = question.difficultyCount,
        qualityCount = question.qualityCount,
        created_time = question.created_time,
        author = question.author,
        active_question = question
    )
    d_question.save()
    return d_question