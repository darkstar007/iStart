from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',    'ideasapp.views.ideas_list', name='ideas_list'),    # For submitting ideas
    url(r'^submit/',    'ideasapp.views.submit', name='submit'),    # For submitting ideas
    url(r'^ideas_cloud/',    'ideasapp.views.ideas_cloud', name='ideas_cloud'),    # For viewing ideas cloud
    url(r'^ideas_list/',    'ideasapp.views.ideas_list', name='ideas_list'),    # For viewing ideas cloud
    url(r'^ideas_gallery/',    'ideasapp.views.ideas_gallery', name='ideas_gallery'),    # For viewing ideas cloud
    url(r'^back/',    'ideasapp.views.back', name='back'),    # For backing an idea
    url(r'^like/(?P<ideaid>\w+)/$',    'ideasapp.views.like', name='like'),    

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
