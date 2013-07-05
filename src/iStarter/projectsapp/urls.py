from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',    'projectsapp.views.project_gallery', name='project_gallery'),                      		# Landing page in projectsapp is the gallery
    url(r'^submit/',    'projectsapp.views.submit', name='submit'),                          				# For creating a new project
    url(r'^project_list/','projectsapp.views.project_list', name='project_list'),             				# For viewing projects as a list
    url(r'^project_gallery/','projectsapp.views.project_gallery', name='project_gallery'),    				# For viewing projects as icon tiles in a table
    url(r'^gallery_filtered/','projectsapp.views.project_gallery_filtered', name='project_gallery_filtered'),    # For viewing projects as icon tiles in a table
    
    url(r'^like/(?P<projectid>\w+)/$', 'projectsapp.views.like', name='like'),								# for saying you like a project
    url(r'^unlike/(?P<projectid>\w+)/$', 'projectsapp.views.unlike', name='unlike'),						# for saying you like a project
    url(r'^project_detail/(?P<projid>\w+)/$','projectsapp.views.project_detail', name='project_detail'),	# Look at the detail of a project
    url(r'^back/(?P<projid>\w+)/$',    'projectsapp.views.back', name='back'),								# For saying you will back a project

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
