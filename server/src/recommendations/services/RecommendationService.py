from datetime import datetime, timedelta
import pytz

from ..models import  Recommendation, RecommendedTopicRole

def get_user_recommendations(course_user, review=False):
    user_recommendations = []
    # 1. Get all the RecommendedTopicRoles where each recommendation has ${course_user} as recommendation.course_user

    recommendations = Recommendation.objects.filter(course_user=course_user) \
        if not review else Recommendation.objects.filter(suggested_course_user=course_user)
    recommended_topic_roles = RecommendedTopicRole.objects.filter(recommendation__in=recommendations)
    # 2. For each rec_top_role in recommended_topic_roles
    for rec_top_role in recommended_topic_roles:

        course_user = rec_top_role.recommendation.suggested_course_user \
            if not review else rec_top_role.recommendation.course_user

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
    current_utc = datetime.utcnow()
    current_weekday = current_utc.weekday()
    # Based off: https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
    days_ahead = day - current_utc.weekday()
    if days_ahead <= 3: # Too close to set event
        days_ahead += 7
    event_utc = current_utc + timedelta(days_ahead)
    # Set the time
    event_utc = event_utc.replace(hour=hour, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
    return event_utc
