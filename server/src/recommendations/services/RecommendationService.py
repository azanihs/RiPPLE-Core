def get_user_find_recommendations(course_user):
    # Get the peer recommendations for the user
    peer_recommendations = PeerRecommendation.objects.filter(course_user=course_user)

    recommendations = []
    for peer_rec in peer_recommendations:

        # Get the connections with that peer recommendation
        connections = Connection.objects.filter(peer_recommendation=peer_rec, user_status="pending")

        if (len(connections) > 0):
            recommendation = {}

            recommendation['recommendedCourseUser'] = peer_rec.recommended_course_user.toJSON()
            recommendation['recommendedRole'] = []
            recommendation['dayTime'] = []
            for connection in connections:
                # Get the topic and study role of the reccommendedCourseUser
                recommended_role = {}
                recommended_role['topic'] = connection.recomended_user_role.topic.toJSON()
                reccomended_role['studyRole'] = connection.recomended_user_role.toJSON()
                recommendation['recommendedRole'].append(recommended_role)

                availability = connection.time_recommendation.recommended_user_availability
                dayTime = {
                        'day': availability.day.toJSON(),
                        'time': availability.time.toJSON()
                }

                recommendation['dayTime'].append(dayTime)

            recommendations.append(recommendation)

    return recommendations

def get_user_review_recommendations(course_user):
    # Get the peer recommendations for the user
    peer_recommendations = PeerRecommendation.objects.filter(
        recommended_course_user=course_user,
        user_status="accepted",
        recommended_user_status="pending"
        )

    recommendations = []
    for peer_rec in peer_recommendations:

        # Get the connections with that peer recommendation
        connections = Connection.objects.filter(peer_recommendation=peer_rec)

        if (len(connections) > 0):
            recommendation = {}

            recommendation['recommendedCourseUser'] = peer_rec.course_user.toJSON()
            recommendation['recommendedRole'] = []
            recommendation['dayTime'] = []
            for connection in connections:
                # Get the topic and study role of the reccommendedCourseUser
                recommended_role = {}
                recommended_role['topic'] = connection.user_role.topic.toJSON()
                reccomended_role['studyRole'] = connection.user_role.toJSON()
                recommendation['recommendedRole'].append(recommended_role)

                availability = connection.time_recommendation.user_availability
                dayTime = {
                        'day': availability.day.toJSON(),
                        'time': availability.time.toJSON()
                }

                recommendation['dayTime'].append(dayTime)

            recommendations.append(recommendation)

    return recommendations
