from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    #url(r'^accounts/',   include('accountsapp.urls')),    # For authentication

    url(r'^$',   include('ideasapp.urls')),    # For ideas
    url(r'^ideas/',   include('ideasapp.urls')),    # For ideas
    url(r'^projects/',   include('projectsapp.urls')),    # For ideas

)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
