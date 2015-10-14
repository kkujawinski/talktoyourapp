from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.home', name='home'),
    url(r'^participants/', include('participants.urls')),
    url(r'^ivr/', include('ivr.urls', namespace='ivr')),
    url(r'^admin/', include(admin.site.urls)),
)
