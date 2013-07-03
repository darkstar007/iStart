from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db.models import Count, Min, Sum, Max, Avg
from django.http import HttpResponse

import os
import sys
import logging
from datetime import datetime
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
from projectsapp.models import pvote as projectVoteModel
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

    #pData = projectModel.objects.annotate(likes = Sum('pvote__like'), backs = Sum('pvote__backer')).order_by('-pub_date').values('id','title','description','pub_date')
    pData = projectModel.objects.order_by('-pub_date').values('id','title','description','pub_date',
                                                               'num_likes', 'num_dislikes', 'num_backers')
    c['headings']=['Project Title','Project Description', 'Date Published', 'Likes', 'Dislikes', 'Backers', 'Vote', 'Back']
    c['tableData'] = pData
    print pData
    return render_to_response("projectsapp/project_list.html", c)
            	
def project_gallery(request):
    ''' Display all the projects as table list of icons'''
    c = {"classification":"unclassified","page_title":"Project Gallery"}
    c.update(csrf(request))
    
    c['headings']=['Idea Title','Date Published','Idea Detail','Number of Backers']
    
    return render_to_response("projectsapp/project_gallery.html", c)	

def like(request, projectid):
    ''' Liking and disliking. '''
    
    #Databases clicks of the like and dislike buttons
    # Has the form been submitted?
    print 'HERE!!'
    if request.method == 'GET': 
        #dislike_ideas183
        #Strip the choice
        splt = projectid.split('_')
        prjid = splt[1]
        print prjid
        choice = splt[0]
        print choice
        if choice in ['like', 'dislike', 'back']:
            print 'Got a vlid choice'
            #Now record this in the db
            pData = projectModel.objects.filter(id=prjid)[0]
            print pData
            newLike = projectVoteModel(project=pData, vote_date=datetime.now(), vote_type = choice)
#            newLike.project.add(pData)

            if choice == 'like':
                pData.num_likes += 1
                
            elif choice == 'dislike':
                pData.num_dislikes += 1
                
            elif choice == 'back':
                pData.num_backers +=1

            xml = '<data><iddata>'+str(prjid)+'</iddata><valdata>cell'+str(choice)+'_'+prjid+'</validate></data>'
            pData.save()
            newLike.save()

#                    xml = '<data><iddata>'+str(numlikes)+'</iddata><valdata>'+'celllike_'+titlehsh+'</valdata></data>'
        print xml
        #not working yet
        #return HttpResponse(xml, mimetype="text/xml")
        return HttpResponse()
    
