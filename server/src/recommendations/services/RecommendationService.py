from datetime import datetime, timedelta
import pytz

from django.http import JsonResponse, HttpResponse

from ..models import  Recommendation, RecommendedTopicRole

def get_user_recommendations(course_user, review=False):
    user_recommendations = []
    # 1. Get all the RecommendedTopicRoles where each recommendation has ${course_user} as recommendation.course_user
    recommendations = Recommendation.objects.filter(course_user=course_user) \
        if not review else Recommendation.objects.filter(suggested_course_user=course_user, user_status="accepted")
    recommended_topic_roles = RecommendedTopicRole.objects.filter(recommendation__in=recommendations)
    # 2. For each rec_top_role in recommended_topic_roles
    for rec_top_role in recommended_topic_roles:
        course_user = rec_top_role.recommendation.suggested_course_user \
            if not review else rec_top_role.recommendation.course_user
        user_recommendation = {
            'id': rec_top_role.recommendation.id,
            'recommendedCourseUser': course_user.toJSON(),
            'recommendedRole': [{
                'topic': rec_top_role.topic.toJSON(),
                'studyRole': rec_top_role.study_role.toJSON()
            }],
            'eventTime': rec_top_role.recommendation.eventTimeToJSON()
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
    recommended_topic_roles = RecommendedTopicRole.objects.filter(recommendation__in=recommendations)
    for rec_top_role in recommended_topic_roles:
        course_user = rec_top_role.recommendation.suggested_course_user
        user_recommendation = {
            'recommendedCourseUser': course_user.toJSON(),
            'recommendedRole': [{
                'topic': rec_top_role.topic.toJSON(),
                'studyRole': rec_top_role.study_role.toJSON()
            }],
            'eventTime': rec_top_role.recommendation.eventTimeToJSON()
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
        update_recommendation_suggested_user_status(rec_id, status)
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

    elif status == "rejected":
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
    elif status == "rejected":
        recommendation.user_status=status
        recommendation.save()
    else:
        return JsonResponse({"state": "Error", "error": "Invalid user status"})

    return JsonResponse({"state": "Recommendation Updated", "recommendation": Recommendation.objects.get(id=rec_id).toJSON()})
