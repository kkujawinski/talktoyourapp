from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^welcome/(?P<participant_id>[\d])/$', views.welcome, name='welcome'),
    url(r'^question/(?P<participant_id>[\d])/$', views.question, name='question'),
    url(r'^answer/(?P<participant_id>[\d])/(?P<question_id>[\d])/$', views.answer, name='answer'),
    url(r'^call_status/$', views.call_status, name='call_status'),
)
