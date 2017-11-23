from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/(.*)$', views.login, name='login'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/update/$', views.update, name='update'),
    url(r'^me/image/$', views.image_update, name='image_update'),
    url(r'^me/$', views.me, name='me'),
    url(r'^ach/$', views.testAch, name="testAch")
    url(r'^getUser/(.*)$', views.getUser, name='getuser')
]
