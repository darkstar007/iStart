from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db.models import Count, Min, Sum, Max, Avg

import os
import sys
import logging
import collections
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
from code import saveTags, distinctTagsSortedAlpha

def submit(request):
    ''' Pulling together ideas into a glorious project. '''

    c = {"classification":"unclassified",
         "page_title":"Submit a Project"}
    c.update(csrf(request))
    
    # Create the tag list for selecting by user
    c['known_tags'] = distinctTagsSortedAlpha()
    
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

            savedProject = saveProject(cleanForm['title'], cleanForm['description'], cleanForm['cls'], cleanForm['ideas'], project_headers)
                                    
            # We can only add tags to a saved object - this saves the structured ones
            res = saveTags(savedProject, cleanForm['new_tags'])
            
            # This saves the unstructured ones
            res = saveTags(savedProject, cleanForm['existing_tags'])

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

    pData = projectModel.objects.annotate(weight = Sum('pvote__weight')).order_by('-weight').values_list('title','description','pub_date', 'weight')

    c['headings']=['Project Title','Project Description', 'Date Published', 'Weight of Backers']
    c['tableData'] = pData
    
    return render_to_response("projectsapp/project_list.html", c)
            	
def project_gallery(request):
	''' Display all the projects as table list of icons'''
	c = {"classification":"unclassified","page_title":"iSTARter Project Gallery"}
	c.update(csrf(request))
	pData = projectModel.objects.values_list('title','pub_date','description', 'num_backers')
	rowdict = {'title':'','pub_date':'','description':'','backPercentage':'','id':''}

 	#Template for model outputs
 	template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'}]
	
	# First find maximum backers todate
	maxbackers= -1
	backers=0
	for pDataidx, row in enumerate(pData):
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='num_backers' :
				backers=row[headingidx]
			if backers > maxbackers :
				maxbackers=backers

	# Prepare the data to pass to the HTML
	outrow = []
	out = []

	for pDataidx, row in enumerate(pData):
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='title' :
				rowdict['title'] = row[headingidx][:20]
			if heading['db']=='pub_date' :
				rowdict['pub_date'] = row[headingidx]
			if heading['db']=='description' :
				rowdict['description'] = row[headingidx][:200]
			if heading['db']=='num_backers' :
				rowdict['backPercentage'] = 100 * row[headingidx] / maxbackers
			if heading['db']=='id' :
				rowdict['id']='project'+str(pDataidx)+str(headingidx)
        	outrow.append(rowdict.copy())
		out.append(outrow)
		outrow = []
	c['tableData'] = out
	c['headings'] = template_headings
	
	return render_to_response("projectsapp/project_gallery.html", c)	
