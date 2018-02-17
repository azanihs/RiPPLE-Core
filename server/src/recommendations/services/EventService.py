from datetime import datetime, timedelta
import pytz as timezone

from ..models import Recommendation, RecommendedTopicRole
from . import RecommendationService

def get_week_events(course_user):
    events = []

    earliest_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    latest_time = (datetime.utcnow() + timedelta(days=6)).replace(tzinfo=timezone.utc)

    recommendations = Recommendation.objects.filter(
        course_user=course_user,
        user_status="accepted",
        suggested_user_status="accepted",
        event_time__gte=earliest_time,
        event_time__lte=latest_time,
        ).order_by("event_time")

    for recommendation in recommendations:
        rec_top_rols = RecommendedTopicRole.objects.filter(
            recommendation=recommendation,
            course_user=recommendation.suggested_course_user)

        topics = []
        for rec_top_rol in rec_top_rols:
            topics.append(rec_top_rol.topic.toJSON())

        event = {
            "id": recommendation.id,
            "time": recommendation.event_time,
            "user": course_user.user.toJSON(),
            "topics": topics,
            "location": recommendation.location
        }

        events.append(event)

    return events

def update_event_status(course_user, rec_id, status):
    rec = Recommendation.objects.get(id=rec_id)
    status_field = "user" if rec.course_user == course_user else "suggested_user"
    return RecommendationService.update_recommendation(status_field=status_field, rec_id=rec_id, status=status)
