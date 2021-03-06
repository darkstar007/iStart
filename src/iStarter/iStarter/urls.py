from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    #url(r'^accounts/',   include('accountsapp.urls')),    	# For authentication

    url(r'^$',   include('projectsapp.urls')),    			# Site landing is passed to projectsapp
    url(r'^ideas/',   include('ideasapp.urls')),    		# krazee ideas for R&D
    url(r'^projects/',   include('projectsapp.urls')),  	# project looking for backing or in development
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
