from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/(.*)$', views.login, name='login'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/update/$', views.update, name='update'),
    url(r'^me/image/$', views.image_update, name='image_update'),
    url(r'^me/$', views.me, name='me'),
    url(r'^get_user/(.*)$', views.get_user, name='get_user'),
    url(r'^achievements/progress/$', views.get_all_user_achievements, name="get_all_user_achievements"),
    url(r'^engagement/$', views.engagement),
    url(r'^engagement/all/$', views.engagement_all),
    url(r'^engagement/aggregate/(.*)/$', views.engagement_aggregate),
    url(r'^consent/$', views.consent, name='consent'),
    url(r'^submit_consent_form/$', views.submit_consent_form, name='submit_consent_form'),
    url(r'^consent_form/$', views.consent_form, name='consent_form'),
    url(r'^has_consented/$', views.has_consented, name='has_consented')
]
