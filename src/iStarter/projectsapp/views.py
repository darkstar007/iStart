from django.shortcuts import render_to_response
from django.core.context_processors import csrf

import os
import sys
import logging
#============================================================================================
# TO ENSURE ALL OF THE FILES CAN SEE ONE ANOTHER.

appRoot = os.path.dirname(os.path.realpath(__name__))

# Find out whats in this directory recursively
for root, subFolders, files in os.walk(appRoot):
    # Loop the folders listed in this directory
    for folder in subFolders:
        directory = os.path.join(root, folder)
        if directory.find('.git') == -1:
            if directory not in sys.path:
                sys.path.append(directory)

#============================================================================================

from projectsapp.models import project as projectModel
from projectsapp.forms import projectForm
from code import formatSubmitterEmail, formatHttpHeaders, getDate, saveProject

def submit(request):
    ''' Pulling together ideas into a glorious project. '''

    c = {"classification":"unclassified",
         "page_title":"My Glorious Project"}
    c.update(csrf(request))
    # Has the form been submitted?
    if request.method == 'POST':
        
        form = projectForm(request.POST)
        
        if form.is_valid():

            # Instantiate an idea
            project = projectModel()

            # Proper Header and django-based user
            headers = request.META
            #user = str(request.user)
            
            # Form content extracted            
            cleanForm = form.cleaned_data

            project_headers = formatHttpHeaders(headers)

            res = saveProject(cleanForm['title'], cleanForm['description'], cleanForm['cls'], cleanForm['ideas'], project_headers)
            #idea.email_starter = formatSubmitterEmail(user)
            # For the output page
            c['title'] = project.title
            c["description"] = project.description
            c['classification'] = project.classification
                
            return render_to_response('projectsapp/project_thanks.html', c)
    
        else:
            logging.error("User failed to enter valid content into form.")
            c['form'] = form
            return render_to_response("projectsapp/project_submit.html", c)
        
    else:
        form = projectForm()
        c.update({"form": form})

    return render_to_response('projectsapp/project_submit.html', c)

def project_list(request):     
    c = {"classification":"unclassified",
         "page_title":"All Projects"}
    c.update(csrf(request))
    # There has to be a better way of doing this! But this will do for now.
    
    rData = projectModel.objects.raw('SELECT projectsapp_project.id,title, description,pub_date, SUM(weight) as tweight FROM projectsapp_project, projectsapp_pvote WHERE projectsapp_project.id = projectsapp_pvote.project_id GROUP BY projectsapp_project.id,title, description,pub_date ORDER by tweight DESC') #projectModel.objects.values_list('title','description','pub_date', 'num_backers')
    pData = []
    for x in rData:
        #pData.append({'title':x.title, 'description': x.description, 'pub_date': x.pub_date, 'weight': x.tweight})
        pData.append([x.title, x.description, x.pub_date, x.tweight])
    c['headings']=['Project Title','Project Description', 'Date Published', 'Weight of Backers']
    c['tableData'] = pData
    
    return render_to_response("projectsapp/project_list.html", c)
            	
def project_gallery(request):
	''' Display all the projects as table list of icons'''
	c = {"classification":"unclassified","page_title":"Project Gallery"}
	c.update(csrf(request))

	c['headings']=['Idea Title','Date Published','Idea Detail','Number of Backers']

	return render_to_response("projectsapp/project_gallery.html", c)	
