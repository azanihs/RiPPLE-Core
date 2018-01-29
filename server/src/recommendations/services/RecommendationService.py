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
            'courseUser': course_user.toJSON(),
            'recommendedRole': {
                'topic': rec_top_role.topic.toJSON(),
                'studyRole': rec_top_role.study_roletoJSON()
            },
            'daytime': {
                    'day': availability.day.toJSON(),
                    'time': availability.time.toJSON()
            }
        }

        user_recommendations.append(user_recommendation)
        return recommendations
