from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',    'projectsapp.views.submit', name='submit'),    # For submitting ideas
    url(r'^submit/',    'projectssapp.views.submit', name='submit'),    # For submitting ideas
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
