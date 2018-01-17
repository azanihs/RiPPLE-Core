from django.db.models import Count, Max

from users.models import CourseUser, User
from questions.models import Topic
from recommendations.models import Day, Time, Availability, StudyRole, Request

# from ..models import Day, Time, Availability, StudyRole, Request

def course_popularity_weightings(course):

    role_popularity = Request.objects.values('topic', 'study_role').annotate(entries=Count('id'))
    max_entries = role_popularity.aggregate(Max('entries'))['entries__max']

    role_counts = []
    for role_entries in role_popularity:
        role_count = {
            'topic': role_entries['topic'],
            'studyRole': role_entries['study_role'],
            'entries': role_entries['entries']
        }
        role_counts.append(role_count)

    course_role_count = {
        'counts': role_counts,
        'max': max_entries
    }

    return course_role_count
