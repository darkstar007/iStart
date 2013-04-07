from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',    'ideasapp.views.submit', name='submit'),    # For submitting ideas
    url(r'^submit/',    'ideasapp.views.submit', name='submit'),    # For submitting ideas
    url(r'^ideas_cloud/',    'ideasapp.views.ideas_cloud', name='ideas_cloud'),    # For viewing ideas cloud

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()