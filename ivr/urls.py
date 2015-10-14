from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^call/(?P<participant_id>[\d])/$', views.initiate_call, name='initiate_call'),
    url(r'^welcome/(?P<participant_id>[\d])/$', views.welcome, name='welcome'),
    url(r'^question/(?P<participant_id>[\d])/$', views.question, name='question'),
    url(r'^answer/(?P<participant_id>[\d])/(?P<question_id>[\d])/$', views.answer, name='answer'),
)
