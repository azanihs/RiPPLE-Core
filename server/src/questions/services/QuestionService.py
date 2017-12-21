import random
import math
import numpy as np
import pytz as timezone
from datetime import datetime

from django.db.models import Count, Min, Max
from django.db import IntegrityError, transaction

from ripple.util import util
from users.models import CourseUser, Token, User, Role, Consent, ConsentForm
from questions.models import Question, Topic, Distractor, QuestionRating, QuestionResponse,\
    Competency, QuestionScore, ReportQuestion, ReportReason, ReportQuestionList, DeletedQuestion
from rippleAchievements.models import UserAchievement
from questions.services import CompetencyService, AuthorService
from users.services import UserService

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

def get_course_leaders(user, has_consented, sort_field, sort_order, limit=25):
    if not type(sort_field) == list:
        sort_field = [sort_field]
    leaderboard_users = create_leaderboard(user, has_consented, sort_field, sort_order)

    found_user = [x for x in leaderboard_users if x["id"] == user.id]
    if found_user:
        found_user = found_user[0]

    for l_user in leaderboard_users:
        if found_user is not l_user:
            l_user.pop("lastName", None)
            l_user.pop("id", None)

    if limit == -1:
        return leaderboard_users

    leaderboard = leaderboard_users[0:limit]
    if not util.is_administrator(user) and found_user not in leaderboard:
        leaderboard.append(found_user)

    return leaderboard

def create_leaderboard(user, has_consented, sort_field, sort_order):
    def lookup_total(fieldName, user_id, data):
        for dict_item in data:
            entry = dict_item.get(fieldName, None)
            if entry == user_id:
                return dict_item.get("total", 0)
        return 0

    course = user.course

    course_users = CourseUser.objects.filter(course=course)
    consent_form = ConsentForm.objects.filter(author__in=course_users).order_by("-created_at").first()
    course_users = course_users.exclude(\
        id__in = CourseUser.objects.filter(roles__in=Role.objects.filter(role="Instructor")))
    if has_consented:
        course_users = course_users.filter(id__in=Consent.objects.filter(
            form=consent_form, response=True).values("user_id"))

    leaderboard_results = _leaderboard_results(course, course_users)

    leaderboard_users = [{
        "id": u.id,
        "firstName": u.user.first_name,
        "lastName": u.user.last_name,
        "image": u.user.image,
        "questionsAuthored": lookup_total(
            "author_id", u.id, leaderboard_results["question_counts"]),
        "questionsAnswered": lookup_total(
            "user_id", u.id, leaderboard_results["response_counts"]),
        "questionsAnsweredCorrectly": lookup_total(
            "user_id", u.id, leaderboard_results["first_response_counts"]),
        "questionsRated": lookup_total(
            "user_id", u.id, leaderboard_results["rating_counts"]),
        "achievementsEarned": lookup_total(
            "user_id", u.id, leaderboard_results["achievement_counts"])
    } for u in course_users]

    sort_fields_exist = set(sort_field).issubset(set(leaderboard_users[0].keys()))

    if len(leaderboard_users) > 0 and sort_fields_exist:
        should_reverse = sort_order == "DESC"
        sort_key = lambda k: tuple(k[i] for i in sort_field)
        leaderboard_users = sorted(
            leaderboard_users, key=sort_key, reverse=should_reverse)

    for i, person in enumerate(leaderboard_users):
        person["rank"] = i+1

    return leaderboard_users


def get_course_topics(course):
    return Topic.objects.filter(course=course).distinct()


def get_random_question(user):
    course = user.course
    course_questions = Question.objects.filter(author__in=CourseUser.objects.filter(course=course))

    count = course_questions.aggregate(count=Count('id'))['count']
    random_index = random.randint(0, count - 1)
    return course_questions.all()[random_index]

def next_recommended_question(user):
    course = user.course
    course_questions = Question.objects.filter(author__in=CourseUser.objects.filter(course=course))
    unanswered_questions = course_questions.exclude(
        id__in=(Distractor.objects.filter(
            id__in=QuestionResponse.objects.filter(user=user).values("response")).values("question")))
    unanswered_ids = [x[0] for x in unanswered_questions.values_list("id")]
    if len(unanswered_ids) == 0:
        return get_random_question(user)
    user_rating = user.elo_rating
    rawSQL = "SELECT *, abs(elo_difficulty-"+str(user_rating)+") AS rating_diff FROM questions_question WHERE id IN ("+\
        ','.join(map(str,unanswered_ids)) + ") ORDER BY rating_diff ASC"
    res = Question.objects.raw(rawSQL)

    if len(list(res)) < 5:
        return get_random_question(user)
    res = list(res)[:5]
    q = random.choice(res)
    return q

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
    update_competency(user, answered_option.question, response)

    if QuestionResponse.objects.filter(
            user=user, response__in=answered_option.question.distractor_set.all()).count() == 1:
        update_ELO(user, answered_option.question, answered_option.isCorrect)
    return True

def update_ELO(user, question, correct):
    user_rating = user.elo_rating
    question_rating = question.elo_difficulty
    # Scalar for measuring change per calculation
    k_factor = 32

    user_r = 10**(user_rating/400)
    question_r = 10**(question_rating/400)

    user_e = user_r / (user_r + question_r)
    question_e = question_r / (user_r + question_r)

    if correct:
        user_s = 1
        question_s = 0
    else:
        user_s = 0
        question_s = 1

    user_rating = user_rating + k_factor * (user_s - user_e)
    question_rating = question_rating + k_factor * (question_s - question_e)

    user.elo_rating = user_rating
    user.save()

    question.elo_difficulty = question_rating
    question.save()

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

def _leaderboard_results(course, course_users):
    question_counts = leaderboard_sort(Question, "author_id")

    response_qry = course_users.annotate(total=Count("questionresponse__response__question", distinct=True))
    response_counts = [{"user_id": r.id, "total": r.total} for r in response_qry]

    first_response_SQL = '''SELECT 1 as id, qr.user_id, COUNT(*) as 'total' FROM questions_questionresponse qr,
        questions_question q, questions_distractor d, users_courseuser cu WHERE d.question_id = q.id AND
        qr.response_id=d.id AND q.author_id=cu.id AND cu.course_id=%s AND d.isCorrect=1 AND qr.id IN (
            SELECT MIN(qr.ID) FROM questions_questionresponse qr, questions_question q,
            questions_distractor d, users_courseuser cu where d.question_id = q.id AND
            qr.response_id=d.id AND q.author_id=cu.id AND cu.course_id=%s GROUP BY qr.user_id,
            q.id)
        GROUP BY qr.user_id'''
    first_response_qry = QuestionResponse.objects.raw(first_response_SQL,[course.id, course.id])
    first_response_counts=[{"user_id": r.user_id, "total": r.total} for r in first_response_qry]

    rating_counts = leaderboard_sort(QuestionRating, "user_id")

    achievement_counts = leaderboard_sort(UserAchievement, "user_id")

    return {
        "question_counts": question_counts,
        "response_counts": response_counts,
        "first_response_counts": first_response_counts,
        "rating_counts": rating_counts,
        "achievement_counts": achievement_counts
    }