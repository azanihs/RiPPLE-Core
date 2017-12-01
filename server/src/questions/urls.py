from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),

    url(r'^respond/$', views.respond, name='respond'),
    url(r'^rate/$', views.rate, name='rate'),

    url(r'^id/(.*)/$', views.id),

    url(r'^competencies/all/$', views.competencies),
    url(r'^competencies/aggregate/(.*)/$', views.aggregate),

    url(r'^add/$', views.add),

    url(r'^distribution/(.*)/$', views.distribution),

    url(r'^leaderboard/$', views.leaderboard_default),
    url(r'^leaderboard/(.*)/(.*)/$', views.leaderboard),

    url(r'^search/$', views.search)
]
