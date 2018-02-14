from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^availability/all/$', views.course_availability),
    url(r'^availability/days/$', views.days),
    url(r'^availability/times/$', views.utc_times),
    url(r'^availability/$', views.user_availability),
    url(r'^availability/update/$', views.update_availability),

    url(r'^roles/all', views.study_roles),
    url(r'^roles/$', views.user_roles),
    url(r'^roles/course', views.role_availability),
    url(r'^roles/update/$', views.update_role),

    url(r'^recommendations/find/all/$', views.get_user_recommendations),
    url(r'^recommendations/pending/all/$', views.get_pending_recommendations),
    url(r'^recommendations/review/all/$', views.get_user_review_recommendations),

    url(r'^recommendations/find/update/$', views.update_recommendation_user_status),
    url(r'^recommendations/review/update/$', views.update_recommendation_suggested_user_status),

    url(r'^recommendations/events/week/$', views.get_week_events),
    url(r'^recommendations/events/update/$', views.update_event_status)

]
