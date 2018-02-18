from datetime import datetime, timedelta
import pytz
from random import randint

from django.http import JsonResponse, HttpResponse

from ..models import Day, Time, Recommendation, RecommendedTopicRole, StudyRole
from users.models import CourseUser
from questions.models import Topic

def get_user_recommendations(course_user, review=False):
    user_recommendations = []
    # 1. Get all the RecommendedTopicRoles where each recommendation has ${course_user} as recommendation.course_user
    recommendations = Recommendation.objects.filter(course_user=course_user, user_status="pending", suggested_user_status="pending") \
        if not review else Recommendation.objects.filter(suggested_course_user=course_user, user_status="accepted", suggested_user_status="pending")

    recommended_topic_roles = RecommendedTopicRole.objects.filter(recommendation__in=recommendations,
        course_user__in=recommendations.values("suggested_course_user")) \
        if not review else RecommendedTopicRole.objects.filter(recommendation__in=recommendations,
        course_user__in=recommendations.values("course_user"))

    # 2. For each rec_top_role in recommended_topic_roles
    for rec_top_role in recommended_topic_roles:
        course_user = rec_top_role.recommendation.suggested_course_user \
            if not review else rec_top_role.recommendation.course_user

        location = "" if not review else rec_top_role.recommendation.location

        user_recommendation = {
            'id': rec_top_role.recommendation.id,
            'recommendedCourseUser': course_user.toJSON(),
            'recommendedRole': [{
                'topic': rec_top_role.topic.toJSON(),
                'studyRole': rec_top_role.study_role.toJSON()
            }],
            'eventTime': rec_top_role.recommendation.eventTimeToJSON(),
            'location': location
        }
        user_recommendations.append(user_recommendation)
    return user_recommendations

def get_pending_recommendations(course_user):
    user_status="accepted"
    suggested_user_status = "pending"
    user_recommendations = []
    recommendations = Recommendation.objects.filter(
        course_user=course_user,
        user_status=user_status,
        suggested_user_status=suggested_user_status)
    recommended_topic_roles = RecommendedTopicRole.objects.filter(recommendation__in=recommendations,
        course_user__in=recommendations.values("suggested_course_user"))
    for rec_top_role in recommended_topic_roles:
        course_user = rec_top_role.recommendation.suggested_course_user
        user_recommendation = {
            'recommendedCourseUser': course_user.toJSON(),
            'recommendedRole': [{
                'topic': rec_top_role.topic.toJSON(),
                'studyRole': rec_top_role.study_role.toJSON()
            }],
            'eventTime': rec_top_role.recommendation.eventTimeToJSON(),
            'location': rec_top_role.recommendation.location
        }
        user_recommendations.append(user_recommendation)
    return user_recommendations

def get_event_utc(day, hour):
    minimum_days_grace = 2
    current_utc = datetime.utcnow()
    current_weekday = current_utc.weekday()
    # Based off: https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
    days_ahead = day - current_utc.weekday()
    if days_ahead <= minimum_days_grace: # Too close to set event
        days_ahead += 7
    event_utc = current_utc + timedelta(days_ahead)
    # Set the time
    event_utc = event_utc.replace(hour=hour, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
    return event_utc

def update_recommendation(status_field, rec_id, status, location=None):
    if status_field == "user":
        return update_recommendation_user_status(rec_id, status, location)
    elif status_field == "suggested_user":
        return update_recommendation_suggested_user_status(rec_id, status)
    else:
        return JsonResponse({"state": "Error", "error": "Invalid user status"})

def update_recommendation_user_status(rec_id, status, location=None):
    try:
        recommendation = Recommendation.objects.get(id=rec_id)
    except Recommendation.DoesNotExist:
        return JsonResponse({"state": "Error", "error": "Recommendation does not exist"})

    if status == "accepted":
        if location is not None:
            recommendation.user_status=status
            recommendation.location=location
            recommendation.save()
        else:
            return JsonResponse({"state": "Error", "error": "Accepted recommendation does not have location"})

    elif status == "rejected" or status == "cancelled":
        recommendation.user_status=status
        recommendation.save()

    else:
        return JsonResponse({"state": "Error", "error": "Invalid user status"})

    return JsonResponse({"state": "Recommendation Updated", "recommendation": Recommendation.objects.get(id=rec_id).toJSON()})

def update_recommendation_suggested_user_status(rec_id, status):
    try:
        recommendation = Recommendation.objects.get(id=rec_id)
    except Recommendation.DoesNotExist:
        return JsonResponse({"state": "Error", "error": "Recommendation does not exist"})

    if status == "accepted":
        recommendation.suggested_user_status=status
        recommendation.save()
    elif status == "rejected" or status == "cancelled":
        recommendation.user_status=status
        recommendation.save()
    else:
        return JsonResponse({"state": "Error", "error": "Invalid user status"})

    return JsonResponse({"state": "Recommendation Updated", "recommendation": Recommendation.objects.get(id=rec_id).toJSON()})

def recommend_study_sessions(course_user):
    # 1. Create new recommendations
    create_recommendations(course_user)
    # 2. Retrieve the recommendations
    return get_user_recommendations(course_user)

# Helper Functions

def get_randomised_day_time():
    days = Day.objects.all()
    times = Time.objects.all()
    random_day = Day.objects.get(pk=randint(1, len(days)))
    random_time = Time.objects.get(pk=randint(1, len(times)))

    return random_day, random_time

def create_recommendations(course_user):
    # TODO: Replace with peer algorithm
    # 1. Get the course_users for a topic
    course_users = CourseUser.objects.filter(course=course_user.course).exclude(id=course_user.id)
    topics = Topic.objects.filter(course=course_user.course)
    suggested_course_user = course_users[randint(0, len(course_users) - 1)]
    user_status = "pending"
    suggested_user_status = "pending"
    topic = topics[randint(0, len(topics) - 1)]
    location = ""

    create_recommendation(
        course_user=course_user,
        suggested_course_user=suggested_course_user,
        user_status=user_status,
        suggested_user_status=suggested_user_status,
        topic=topic,
        location=location)


def get_randomised_study_roles():
    study_roles = StudyRole.objects.all()
    if len(study_roles) == 0:
        return None, None

    user_study_role = study_roles[randint(0, len(study_roles) - 1)]
    suggested_role_filter = "invalid"
    if user_study_role.role == "mentor":
        suggested_role = "mentee"
    elif user_study_role == "mentee":
        suggested_role = "mentor"
    else:
        suggested_role = "partner"

    suggested_user_study_roles = StudyRole.objects.filter(role=suggested_role)
    if len(suggested_user_study_roles) == 0:
        return None, None

    suggested_user_study_role = suggested_user_study_roles[0]

    return user_study_role, suggested_user_study_role

def create_recommended_topic_role(course_user, recommendation, study_role, topic):
        RecommendedTopicRole.objects.create(
            recommendation=recommendation,
            course_user=course_user,
            study_role=study_role,
            topic=topic
        )

def create_recommendation(course_user, suggested_course_user, user_status, suggested_user_status, topic, location=""):

    # Choose a random studyRole
    user_study_role, suggested_user_study_role = get_randomised_study_roles()
    if user_study_role is None or suggested_user_study_role is None:
        return

    # Create a common day and time
    day, time = get_randomised_day_time()

    # TODO: Add the day and time to both users

    event_time = get_event_utc(day.id - 1, time.start.hour)

    recommendation, created = Recommendation.objects.get_or_create(
        course_user=course_user,
        suggested_course_user=suggested_course_user,
        event_time=event_time,
        user_status=user_status,
        suggested_user_status=suggested_user_status,
        location=location,
        score=0
    )

    #create the RecommededTopicRole rows for each user
    create_recommended_topic_role(course_user, recommendation, user_study_role, topic)
    create_recommended_topic_role(suggested_course_user, recommendation, suggested_user_study_role, topic)
